import cv2
import numpy as np
from PIL import Image
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.http import urlencode

from app.models import Customer, Crop, Contact
from config import settings
from config.settings import STATICFILES_DIRS, MODEL_DIRS
import tensorflow as tf

# Create your views here.
def home(request):
    return render(request, 'index.html')
def about(request):
    return render(request, 'about.html')
def category(request):
    return render(request, 'category.html')
def contact(request):
    context = {
        'KAKAO_API_KEY': settings.KAKAO_API_KEY
    }
    return render(request,'contact.html', context)

######### 전처리 함수 ###########
def resize_and_crop(img_array,size):
    img = Image.fromarray(img_array)
    img_ratio = img.size[0] / img.size[1]
    ratio = size[0] / size[1]

    if ratio > img_ratio:
        img = img.resize((size[0], int(round(size[0] * img.size[1] / img.size[0]))),
            Image.LANCZOS)
        box = (0, int(round((img.size[1] - size[1]) / 2)), img.size[0],
              int(round((img.size[1] + size[1]) / 2)))
        img = img.crop(box)

    elif ratio < img_ratio:
        img = img.resize((int(round(size[1] * img.size[0] / img.size[1])), size[1]),
            Image.LANCZOS)
        box = (int(round((img.size[0] - size[0]) / 2)), 0,
              int(round((img.size[0] + size[0]) / 2)), img.size[1])
        img = img.crop(box)

    else :
        img = img.resize((size[0], size[1]), Image.LANCZOS)

    return img
def preprocessing(filepath, imgname):
    img = cv2.imread(filepath + imgname, cv2.IMREAD_COLOR)
    # BGR에서 RGB로 변환
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # numpy 배열로 변환
    image_array = np.array(img_rgb)
    output_size = (224, 224)
    resized_image = resize_and_crop(image_array, output_size)
    x_predict = np.array(resized_image).reshape(1,224,224,3)
    return x_predict

######## 로그인/회원가입 함수 #########
def login(request):
    return render(request, 'login.html')

def logout(request):
    if request.session['sessionid'] != None:
        del request.session['sessionid']
    return render(request, 'index.html')

def loginimpl(request):
    id = request.POST['id']
    pwd = request.POST['pwd']
    print(id, pwd)

    ctx = {}
    # ID를 통해 Customer 객체를 조회 한다.
    # 객체 정보가 있으면
    # PWD를 조회 하여 비교 한다.
    # 객체가 없으면 로그인 실패
    # PWD가 틀리면 로그인 싪패
    try:
        cust = Customer.objects.get(id=id)
        if cust.pwd == pwd:
            request.session['sessionid'] = id
            ctx['id'] = id
            ctx['name'] = cust.name
            return render(request, 'index.html', ctx)
        else:
            ctx['alert'] = '입력하신 ID가 존재하지 않거나 비밀번호가 틀립니다.'
            return render(request, 'login.html', ctx)
    except:
        ctx['alert'] = '입력하신 ID가 존재하지 않거나 비밀번호가 틀립니다.'
        return render(request, 'login.html', ctx)

def register(request):
    return render(request, 'register.html')

def registerimpl(request):
    id = request.POST['id']
    pwd = request.POST['pwd']
    name = request.POST['name']
    print(id, pwd, name)
    try:
        # 새로운 Customer를 생성 시도
        Customer.objects.create(id=id, pwd=pwd, name=name)
        # 성공하면 세션을 설정하고 성공 페이지를 렌더링
        request.session['sessionid'] = id
        ctx = {'id': id, 'name': name}
        return render(request, 'index.html', ctx)

    except IntegrityError:
        # 중복된 ID가 있을 경우 처리
        error_message = '이 아이디는 이미 사용 중입니다. 다른 아이디를 선택해주세요.'
        ctx = {'error_message': error_message}
        return render(request, 'register.html', ctx)

def mypage(request):
    id = request.GET['id']
    crops = Crop.objects.filter(userid=id)
    mails = Contact.objects.filter(userid=id)
    cust = Customer.objects.get(id=id)
    print('mypage:',id)
    ctx = {
        'id':id,
        'getcrops':crops,
        'getcust': cust,
        'getmails':mails,
    }
    return render(request, 'mypage.html', ctx)
def mypageupdate(request):
    id = request.POST['id']
    pwd = request.POST['pwd']
    name = request.POST['name']
    print(id, pwd, name)
    cust = Customer(id=id, pwd=pwd, name=name)
    cust.save()
    qstr = urlencode({'id':id})
    # mypage?id=id01
    return HttpResponseRedirect('%s?%s' % ('mypage',qstr))

def mail(request):
    if request.session.get('sessionid') is not None:
        userid = request.session['sessionid']
        username = request.POST['contact-name']
        email = request.POST['contact-email']
        subject = request.POST['contact-subject']
        message = request.POST['message']
        Contact.objects.create(userid=userid, username=username, email=email, subject=subject, message=message)
        ctx = {
            'result': 'success'
        }
    elif request.session.get('sessionid') == None:
        ctx = {'result':'fail'}
    return render(request, 'contact.html', ctx)

class Cabbage:
    def cabbage(request):
        return render(request, 'input/cabbage.html')
    def analysis(request):
        imgname = ''
        # 예시에 따라 이미지 선택
        example = request.GET.get('example', None)
        if example:
            if example == 'ex1':
                filepath = STATICFILES_DIRS[3]
                imgname = 'cabbage_ex1.jpg'
            elif example == 'ex2':
                filepath = STATICFILES_DIRS[3]
                imgname='cabbage_ex2.jpg'
            elif example == 'ex3':
                filepath = STATICFILES_DIRS[3]
                imgname='cabbage_ex3.jpg'
        elif 'img' in request.FILES:
            # 직접 업로드한 이미지 사용
            uploadimg = request.FILES['img']
            imgname = uploadimg._name
            fp = open('%s%s' % (STATICFILES_DIRS[2], uploadimg), 'wb')
            for temp in uploadimg.chunks():
                fp.write(temp)
            fp.close()
            filepath = STATICFILES_DIRS[2]
        # 전처리
        x_predict = preprocessing(filepath, imgname)
        x_predict = x_predict.astype(np.float32)
        # 모델에 분석 요청
        model = tf.saved_model.load(MODEL_DIRS[1])
        # 추론 (예측)
        inference = model.signatures["serving_default"]
        y_predict = inference(tf.constant(x_predict))
        y_predict = y_predict['dense_1'].numpy()
        # 결과 출력
        print("Predictions:", y_predict)
        # 정상 확률
        good = round(y_predict[0][0]*100, 2)
        bad1 = round(y_predict[0][1]*100, 2)
        bad2 = round(y_predict[0][2]*100, 2)
        if request.session.get('sessionid') is not None and 'img' in request.FILES:
            userid = request.session['sessionid']
            category = '양배추'
            if good >= 80:
                condition = '정상'
            elif good >= 50:
                if bad1 > bad2:
                    condition = '정상-균핵병가능'
                elif bad2 > bad1:
                    condition = '정상-무름병가능'
            else:
                if bad1>bad2:
                    condition = '균핵병'
                elif bad2>bad1:
                    condition = '무름병'
            Crop.objects.create(userid=userid, category=category, condition=condition, imgname=imgname)

        ctx = {
            'result': y_predict,
            'good':good,
            'bad1':bad1,
            'bad2':bad2,
            'filepath': filepath,
            'imgname':imgname,
            'settings':settings,
        }
        return render(request, 'output/cabbage_out.html', ctx)

class Pumpkin:
    def pumpkin(request):
        return render(request, 'input/pumpkin.html')
    def analysis(request):
        imgname = ''
        # 예시에 따라 이미지 선택
        example = request.GET.get('example', None)
        if example:
            if example == 'ex1':
                filepath = STATICFILES_DIRS[3]
                imgname='p_ex1.jpg'
            elif example == 'ex2':
                filepath = STATICFILES_DIRS[3]
                imgname = 'p_ex2.jpg'
            elif example == 'ex3':
                filepath = STATICFILES_DIRS[3]
                imgname = 'p_ex3.jpg'
        elif 'img' in request.FILES:
            # 직접 업로드한 이미지 사용
            uploadimg = request.FILES['img']
            imgname = uploadimg._name
            fp = open('%s%s' % (STATICFILES_DIRS[2], uploadimg), 'wb')
            for temp in uploadimg.chunks():
                fp.write(temp)
                fp.close()
            filepath = STATICFILES_DIRS[2]
        # 전처리
        x_predict = preprocessing(filepath, imgname)
        x_predict = x_predict.astype(np.float32)
        # 모델에 분석 요청
        model = tf.saved_model.load(MODEL_DIRS[2])
        # 추론 (예측)
        inference = model.signatures["serving_default"]
        y_predict = inference(tf.constant(x_predict))
        y_predict = y_predict['dense_3'].numpy()
        # 결과 출력
        print("Predictions:", y_predict)
        # 정상 확률
        good = round(y_predict[0][0]*100, 2)
        bad1 = round(y_predict[0][1]*100, 2)
        bad2 = round(y_predict[0][2]*100, 2)
        if request.session.get('sessionid') is not None and 'img' in request.FILES:
            userid = request.session['sessionid']
            category = '호박'
            if good >= 80:
                condition = '정상'
            elif good >= 50:
                if bad1 > bad2:
                    condition = '정상-노균병가능'
                elif bad2 > bad1:
                    condition = '정상-흰가루병가능'
            else:
                if bad1>bad2:
                    condition = '노균병'
                elif bad2>bad1:
                    condition = '흰가루병'
            Crop.objects.create(userid=userid, category=category, condition=condition, imgname=imgname)
        ctx = {
            'result': y_predict,
            'good':good,
            'bad1':bad1,
            'bad2':bad2,
            'filepath': filepath,
            'imgname':imgname,
            'settings':settings,
        }
        return render(request, 'output/pumpkin_out.html', ctx)

class Bean:
    def bean(request):
        return render(request, 'input/bean.html')
    def analysis(request):
        imgname = ''
        # 예시에 따라 이미지 선택
        example = request.GET.get('example', None)
        if example:
            if example == 'ex1':
                filepath = STATICFILES_DIRS[3]
                imgname = 'bean_ex1.jpg'
            elif example == 'ex2':
                filepath = STATICFILES_DIRS[3]
                imgname = 'bean_ex2.jpg'
            elif example == 'ex3':
                filepath = STATICFILES_DIRS[3]
                imgname = 'bean_ex3.jpg'
        elif 'img' in request.FILES:
            # 직접 업로드한 이미지 사용
            uploadimg = request.FILES['img']
            imgname = uploadimg._name
            fp = open('%s%s' % (STATICFILES_DIRS[2], uploadimg), 'wb')
            for temp in uploadimg.chunks():
                fp.write(temp)
                fp.close()
            filepath = STATICFILES_DIRS[2]
        # 전처리
        x_predict = preprocessing(filepath, imgname)
        x_predict = x_predict.astype(np.float32)
        # 모델에 분석 요청
        model = tf.saved_model.load(MODEL_DIRS[3])
        # 추론 (예측)
        inference = model.signatures["serving_default"]
        y_predict = inference(tf.constant(x_predict))
        y_predict = y_predict['dense_1'].numpy()
        # 결과 출력
        print("Predictions:", y_predict)
        # 정상 확률
        good = round(y_predict[0][0]*100, 2)
        bad1 = round(y_predict[0][1]*100, 2)
        bad2 = round(y_predict[0][2]*100, 2)
        if request.session.get('sessionid') is not None and 'img' in request.FILES:
            userid = request.session['sessionid']
            category = '콩'
            if good >= 80:
                condition = '정상'
            elif good >= 50:
                if bad1 > bad2:
                    condition = '정상-콩불마름병가능'
                elif bad2 > bad1:
                    condition = '정상-콩점무늬병가능'
            else:
                if bad1>bad2:
                    condition = '콩불마름병'
                elif bad2>bad1:
                    condition = '콩점무늬병'
            Crop.objects.create(userid=userid, category=category, condition=condition, imgname=imgname)
        ctx = {
            'result': y_predict,
            'good':good,
            'bad1':bad1,
            'bad2':bad2,
            'filepath': filepath,
            'imgname':imgname,
            'settings':settings,
        }
        return render(request, 'output/bean_out.html', ctx)

class Cucumber:
    def cucumber(request):
        return render(request, 'input/cucumber.html')
    def analysis(request):
        imgname = ''
        # 예시에 따라 이미지 선택
        example = request.GET.get('example', None)
        if example:
            if example == 'ex1':
                filepath = STATICFILES_DIRS[3]
                imgname = 'cucumber_ex1.jpg'
            elif example == 'ex2':
                filepath = STATICFILES_DIRS[3]
                imgname = 'cucumber_ex2.jpg'
            elif example == 'ex3':
                filepath = STATICFILES_DIRS[3]
                imgname = 'cucumber_ex3.jpeg'
        elif 'img' in request.FILES:
            # 직접 업로드한 이미지 사용
            uploadimg = request.FILES['img']
            imgname = uploadimg._name
            fp = open('%s%s' % (STATICFILES_DIRS[2], uploadimg), 'wb')
            for temp in uploadimg.chunks():
                fp.write(temp)
                fp.close()
            filepath = STATICFILES_DIRS[2]
        # 전처리
        x_predict = preprocessing(filepath, imgname)
        x_predict = x_predict.astype(np.float32)
        # 모델에 분석 요청
        model = tf.saved_model.load(MODEL_DIRS[4])
        # 추론 (예측)
        inference = model.signatures["serving_default"]
        y_predict = inference(tf.constant(x_predict))
        y_predict = y_predict['dense_1'].numpy()
        # 결과 출력
        print("Predictions:", y_predict)
        # 정상 확률
        good = round(y_predict[0][0]*100, 2)
        bad1 = round(y_predict[0][1]*100, 2)
        bad2 = round(y_predict[0][2]*100, 2)
        if request.session.get('sessionid') is not None and 'img' in request.FILES:
            userid = request.session['sessionid']
            category = '오이'
            if good >= 80:
                condition = '정상'
            elif good >= 50:
                if bad1 > bad2:
                    condition = '정상-노균병가능'
                elif bad2 > bad1:
                    condition = '정상-흰가루병가능'
            else:
                if bad1>bad2:
                    condition = '노균병'
                elif bad2>bad1:
                    condition = '흰가루병'
            Crop.objects.create(userid=userid, category=category, condition=condition, imgname=imgname)
        ctx = {
            'result': y_predict,
            'good':good,
            'bad1':bad1,
            'bad2':bad2,
            'filepath': filepath,
            'imgname':imgname,
            'settings':settings,
        }
        return render(request, 'output/cucumber_out.html', ctx)

class Greenonion:
    def greenonion(request):
        return render(request, 'input/greenonion.html')
    def analysis(request):
        imgname = ''
        # 예시에 따라 이미지 선택
        example = request.GET.get('example', None)
        if example:
            if example == 'ex1':
                filepath = STATICFILES_DIRS[3]
                imgname = 'pa_ex1.jpg'
            elif example == 'ex2':
                filepath = STATICFILES_DIRS[3]
                imgname = 'pa_ex2.JPEG'
            elif example == 'ex3':
                filepath = STATICFILES_DIRS[3]
                imgname = 'pa_ex3.jpg'
        elif 'img' in request.FILES:
            # 직접 업로드한 이미지 사용
            uploadimg = request.FILES['img']
            imgname = uploadimg._name
            fp = open('%s%s' % (STATICFILES_DIRS[2], uploadimg), 'wb')
            for temp in uploadimg.chunks():
                fp.write(temp)
                fp.close()
            filepath = STATICFILES_DIRS[2]
        # 전처리
        x_predict = preprocessing(filepath, imgname)
        x_predict = x_predict.astype(np.float32)
        # 모델에 분석 요청
        model = tf.saved_model.load(MODEL_DIRS[5])
        # 추론 (예측)
        inference = model.signatures["serving_default"]
        y_predict = inference(tf.constant(x_predict))
        y_predict = y_predict['dense_3'].numpy()
        # 결과 출력
        print("Predictions:", y_predict)
        # 정상 확률
        good = round(y_predict[0][0]*100, 2)
        bad1 = round(y_predict[0][1]*100, 2)
        bad2 = round(y_predict[0][2]*100, 2)
        bad3 = round(y_predict[0][3]*100, 2)
        if request.session.get('sessionid') is not None and 'img' in request.FILES:
            userid = request.session['sessionid']
            category = '파'
            if good >= 80:
                condition = '정상'
            elif good >= 50:
                if bad1 > bad2 and bad1 > bad3:
                    condition = '정상-검은무늬병가능'
                elif bad2 > bad1 and bad2 > bad3:
                    condition = '정상-노균병가능'
                elif bad3 > bad1 and bad3 > bad2:
                    condition = '정상-녹병가능'
            else:
                if bad1>bad2 and bad1 > bad3:
                    condition = '검은무늬병'
                elif bad2>bad1 and bad2 > bad3:
                    condition = '노균병'
                elif bad3 > bad1 and bad3 > bad2:
                    condition = '녹병'
            Crop.objects.create(userid=userid, category=category, condition=condition, imgname=imgname)
        ctx = {
            'result': y_predict,
            'good':good,
            'bad1':bad1,
            'bad2':bad2,
            'bad3':bad3,
            'filepath': filepath,
            'imgname':imgname,
            'settings':settings,
        }
        return render(request, 'output/greenonion_out.html', ctx)

class Kimchi:
    def kimchi(request):
        return render(request, 'input/kimchi.html')
    def analysis(request):
        imgname = ''
        # 예시에 따라 이미지 선택
        example = request.GET.get('example', None)
        if example:
            if example == 'ex1':
                filepath = STATICFILES_DIRS[3]
                imgname = 'cabbage_ex1.jpg'
            elif example == 'ex2':
                filepath = STATICFILES_DIRS[3]
                imgname = 'cabbage_ex2.jpg'
            elif example == 'ex3':
                filepath = STATICFILES_DIRS[3]
                imgname = 'cabbage_ex3.jpg'
        elif 'img' in request.FILES:
            # 직접 업로드한 이미지 사용
            uploadimg = request.FILES['img']
            imgname = uploadimg._name
            fp = open('%s%s' % (STATICFILES_DIRS[2], uploadimg), 'wb')
            for temp in uploadimg.chunks():
                fp.write(temp)
                fp.close()
            filepath = STATICFILES_DIRS[2]
        # 전처리
        x_predict = preprocessing(filepath, imgname)
        x_predict = x_predict.astype(np.float32)
        # 모델에 분석 요청
        model = tf.saved_model.load(MODEL_DIRS[6])
        # 추론 (예측)
        inference = model.signatures["serving_default"]
        y_predict = inference(tf.constant(x_predict))
        y_predict = y_predict['dense_1'].numpy()
        # 결과 출력
        print("Predictions:", y_predict)
        # 정상 확률
        good = round(y_predict[0][0]*100, 2)
        bad1 = round(y_predict[0][1]*100, 2)
        bad2 = round(y_predict[0][2]*100, 2)
        if request.session.get('sessionid') is not None and 'img' in request.FILES:
            userid = request.session['sessionid']
            category = '배추'
            if good >= 80:
                condition = '정상'
            elif good >= 50:
                if bad1 > bad2:
                    condition = '정상-검은썩음병가능'
                elif bad2 > bad1:
                    condition = '정상-노균병가능'
            else:
                if bad1>bad2:
                    condition = '검은썩음병'
                elif bad2>bad1:
                    condition = '노균병'
            Crop.objects.create(userid=userid, category=category, condition=condition, imgname=imgname)
        ctx = {
            'result': y_predict,
            'good':good,
            'bad1':bad1,
            'bad2':bad2,
            'filepath': filepath,
            'imgname':imgname,
            'settings':settings,
        }
        return render(request, 'output/kimchi_out.html', ctx)

class Pepper:
    def pepper(request):
        return render(request, 'input/pepper.html')
    def analysis(request):
        imgname = ''
        # 예시에 따라 이미지 선택
        example = request.GET.get('example', None)
        if example:
            if example == 'ex1':
                filepath = STATICFILES_DIRS[3]
                imgname = 'pepper_ex1.JPEG'
            elif example == 'ex2':
                filepath = STATICFILES_DIRS[3]
                imgname = 'pepper_ex2.JPG'
            elif example == 'ex3':
                filepath = STATICFILES_DIRS[3]
                imgname = 'pepper_ex3.jpg'
        elif 'img' in request.FILES:
            # 직접 업로드한 이미지 사용
            uploadimg = request.FILES['img']
            imgname = uploadimg._name
            fp = open('%s%s' % (STATICFILES_DIRS[2], uploadimg), 'wb')
            for temp in uploadimg.chunks():
                fp.write(temp)
                fp.close()
            filepath = STATICFILES_DIRS[2]
        # 전처리
        x_predict = preprocessing(filepath, imgname)
        x_predict = x_predict.astype(np.float32)
        # 모델에 분석 요청
        model = tf.saved_model.load(MODEL_DIRS[7])
        # 추론 (예측)
        inference = model.signatures["serving_default"]
        y_predict = inference(tf.constant(x_predict))
        y_predict = y_predict['dense_3'].numpy()
        # 결과 출력
        print("Predictions:", y_predict)
        # 정상 확률
        good = round(y_predict[0][0]*100, 2)
        bad1 = round(y_predict[0][1]*100, 2)
        bad2 = round(y_predict[0][2]*100, 2)
        if request.session.get('sessionid') is not None and 'img' in request.FILES:
            userid = request.session['sessionid']
            category = '고추'
            if good >= 80:
                condition = '정상'
            elif good >= 50:
                if bad1 > bad2:
                    condition = '정상-탄저병가능'
                elif bad2 > bad1:
                    condition = '정상-흰가루병가능'
            else:
                if bad1>bad2:
                    condition = '탄저병'
                elif bad2>bad1:
                    condition = '흰가루병'
            Crop.objects.create(userid=userid, category=category, condition=condition, imgname=imgname)
        ctx = {
            'result': y_predict,
            'good':good,
            'bad1':bad1,
            'bad2':bad2,
            'filepath': filepath,
            'imgname':imgname,
            'settings':settings,
        }
        return render(request, 'output/pepper_out.html', ctx)

class Radish:
    def radish(request):
        return render(request, 'input/radish.html')
    def analysis(request):
        imgname = ''
        # 예시에 따라 이미지 선택
        example = request.GET.get('example', None)
        if example:
            if example == 'ex1':
                filepath = STATICFILES_DIRS[3]
                imgname = 'radish_ex1.jpg'
            elif example == 'ex2':
                filepath = STATICFILES_DIRS[3]
                imgname = 'radish_ex2.jpg'
            elif example == 'ex3':
                filepath = STATICFILES_DIRS[3]
                imgname = 'radish_ex3.jpg'
        elif 'img' in request.FILES:
            # 직접 업로드한 이미지 사용
            uploadimg = request.FILES['img']
            imgname = uploadimg._name
            fp = open('%s%s' % (STATICFILES_DIRS[2], uploadimg), 'wb')
            for temp in uploadimg.chunks():
                fp.write(temp)
                fp.close()
            filepath = STATICFILES_DIRS[2]
        # 전처리
        x_predict = preprocessing(filepath, imgname)
        x_predict = x_predict.astype(np.float32)
        # 모델에 분석 요청
        model = tf.saved_model.load(MODEL_DIRS[8])
        # 추론 (예측)
        inference = model.signatures["serving_default"]
        y_predict = inference(tf.constant(x_predict))
        y_predict = y_predict['dense_7'].numpy()
        # 결과 출력
        print("Predictions:", y_predict)
        # 정상 확률
        good = round(y_predict[0][0]*100, 2)
        bad1 = round(y_predict[0][1]*100, 2)
        bad2 = round(y_predict[0][2]*100, 2)
        if request.session.get('sessionid') is not None and 'img' in request.FILES:
            userid = request.session['sessionid']
            category = '무'
            if good >= 80:
                condition = '정상'
            elif good >= 50:
                if bad1 > bad2:
                    condition = '정상-검은무늬병가능'
                elif bad2 > bad1:
                    condition = '정상-노균병가능'
            else:
                if bad1>bad2:
                    condition = '검은무늬병'
                elif bad2>bad1:
                    condition = '노균병'
            Crop.objects.create(userid=userid, category=category, condition=condition, imgname=imgname)
        ctx = {
            'result': y_predict,
            'good':good,
            'bad1':bad1,
            'bad2':bad2,
            'filepath': filepath,
            'imgname' : imgname,
            'settings': settings,
        }
        return render(request, 'output/radish_out.html', ctx)

class Tomato:
    def tomato(request):
        return render(request, 'input/tomato.html')
    def analysis(request):
        imgname = ''
        # 예시에 따라 이미지 선택
        example = request.GET.get('example', None)
        if example:
            if example == 'ex1':
                filepath = STATICFILES_DIRS[3]
                imgname = 'tomato_ex1.jpg'
            elif example == 'ex2':
                filepath = STATICFILES_DIRS[3]
                imgname = 'tomato_ex2.jpg'
            elif example == 'ex3':
                filepath = STATICFILES_DIRS[3]
                imgname = 'tomato_ex3.JPG'
        elif 'img' in request.FILES:
            # 직접 업로드한 이미지 사용
            uploadimg = request.FILES['img']
            imgname = uploadimg._name
            fp = open('%s%s' % (STATICFILES_DIRS[2], uploadimg), 'wb')
            for temp in uploadimg.chunks():
                fp.write(temp)
                fp.close()
            filepath = STATICFILES_DIRS[2]
        # 전처리
        x_predict = preprocessing(filepath, imgname)
        x_predict = x_predict.astype(np.float32)
        # 모델에 분석 요청
        model = tf.saved_model.load(MODEL_DIRS[9])
        # 추론 (예측)
        inference = model.signatures["serving_default"]
        y_predict = inference(tf.constant(x_predict))
        y_predict = y_predict['dense_1'].numpy()
        # 결과 출력
        print("Predictions:", y_predict)
        # 정상 확률
        bad = round(y_predict[0][0]*100, 2)
        good = 100-bad
        if request.session.get('sessionid') is not None and 'img' in request.FILES:
            userid = request.session['sessionid']
            category = '토마토'
            if good >= 80:
                condition = '정상'
            elif good >= 50:
                condition = '정상-잎마름병가능'
            else:
                condition = '잎마름병'
            Crop.objects.create(userid=userid, category=category, condition=condition, imgname=imgname)
        ctx = {
            'result': y_predict,
            'bad':bad,
            'good':good,
            'filepath': filepath,
            'imgname':imgname,
            'settings':settings,
        }
        return render(request, 'output/tomato_out.html', ctx)

class Youngpumpkin:
    def youngpumpkin(request):
        return render(request, 'input/youngpumpkin.html')
    def analysis(request):
        imgname = ''
        # 예시에 따라 이미지 선택
        example = request.GET.get('example', None)
        if example:
            if example == 'ex1':
                filepath = STATICFILES_DIRS[3]
                imgname = 'youngpumpkin_ex1.jpg'
            elif example == 'ex2':
                filepath = STATICFILES_DIRS[3]
                imgname = 'youngpumpkin_ex2.jpg'
            elif example == 'ex3':
                filepath = STATICFILES_DIRS[3]
                imgname = 'youngpumpkin_ex3.jpg'
        elif 'img' in request.FILES:
            # 직접 업로드한 이미지 사용
            uploadimg = request.FILES['img']
            imgname = uploadimg._name
            fp = open('%s%s' % (STATICFILES_DIRS[2], uploadimg), 'wb')
            for temp in uploadimg.chunks():
                fp.write(temp)
                fp.close()
            filepath = STATICFILES_DIRS[2]
        # 전처리
        x_predict = preprocessing(filepath, imgname)
        x_predict = x_predict.astype(np.float32)
        # 모델에 분석 요청
        model = tf.saved_model.load(MODEL_DIRS[10])
        # 추론 (예측)
        inference = model.signatures["serving_default"]
        y_predict = inference(tf.constant(x_predict))
        y_predict = y_predict['dense_3'].numpy()
        # 결과 출력
        print("Predictions:", y_predict)
        # 정상 확률
        good = round(y_predict[0][0]*100, 2)
        bad1 = round(y_predict[0][1]*100, 2)
        bad2 = round(y_predict[0][2]*100, 2)
        if request.session.get('sessionid') is not None and 'img' in request.FILES:
            userid = request.session['sessionid']
            category = '애호박'
            if good >= 80:
                condition = '정상'
            elif good >= 50:
                if bad1 > bad2:
                    condition = '정상-노균병가능'
                elif bad2 > bad1:
                    condition = '정상-흰가루병가능'
            else:
                if bad1>bad2:
                    condition = '노균병'
                elif bad2>bad1:
                    condition = '흰가루병'
            Crop.objects.create(userid=userid, category=category, condition=condition, imgname=imgname)
        ctx = {
            'result': y_predict,
            'good':good,
            'bad1':bad1,
            'bad2':bad2,
            'filepath': filepath,
            'imgname':imgname,
            'settings':settings,
        }
        return render(request, 'output/youngpumpkin_out.html', ctx)