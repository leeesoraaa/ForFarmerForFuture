# 🌱 For Farmer For Future (F4)

**농작물 질병 진단 및 재배 가이드 웹 플랫폼**

<img src="https://img.shields.io/badge/Framework-Django-green" /> <img src="https://img.shields.io/badge/AI-TensorFlow-blue" /> <img src="https://img.shields.io/badge/Deployment-PythonAnywhere-orange" />

---

## 📌 프로젝트 개요

농업 창업을 고려하는 예비 농부와 초보 농부들을 위한 **노지 작물(배추, 무, 파 등 10종)의 질병 진단 및 재배 가이드 웹 서비스**입니다.  
이미지 기반 AI 모델을 활용해 작물 상태를 진단하고, 재배 방법과 병해충 해결책을 제공하여 농업 진입 장벽을 낮추고자 합니다.

---

## 🧠 핵심 기술

- **데이터**: AIHub 제공 작물 질병 이미지 데이터셋 (320,000건)
- **전처리**: 크롭/리사이즈, RGB 축소, 불균형 데이터 처리
- **모델**: ResNet (최적 구조: 17-layer, accuracy 99.2%, size 95MB)
- **웹**: Django 기반 웹 구현 + PythonAnywhere 배포
- **시각화**: jQuery barfiller를 활용한 예측 결과 시각화

---

## 🖥 주요 기능

### ✅ 회원 기능
- 회원가입 / 로그인
- 작물 진단 이력 확인
- 문의/답변 기록 확인 및 프로필 수정

### 🌿 작물 진단
- 10종 작물 업로드 기반 질병 진단
- 예측 확률 시각화 (정상/질병1/질병2)
- AI 모델 기반 실시간 분석 결과 제공

### 📷 작물 가이드
- 작물별 재배법 / 효능 / 활용법 제공
- YouTube 영상 링크로 시각적 가이드 제공

### 📬 문의 기능
- 로그인 기반 관리자 문의 및 답장 기능
- Django ORM 기반 DB 관리 (Customer, Crop, Contact 모델)

---

## 📂 기술 스택

| 구분 | 사용 기술 |
|------|-----------|
| 언어 | Python 3.9 |
| AI | TensorFlow 2.15, ResNet |
| 전처리 | Pandas, NumPy, Pillow, OpenCV |
| 웹 | Django 4.0.6, Bootstrap Template |
| 배포 | PythonAnywhere |
| 기타 | jQuery, Kakao Map API, HTML/CSS |

---

## 🗃 데이터 정보

- 정상 이미지: 100,000건
- 질병 이미지(원본): 20,000건
- 질병 이미지(증강): 200,000건
- 총 10개 작물, 32만 건의 이미지 사용

---

## 📊 모델 성능

| 모델 구조 | 정확도 | 용량 |
|-----------|--------|------|
| ResNet-18 | 99.1% | 151MB |
| ResNet-34 | 99.4% | 267MB |
| ResNet-50 | 99.5% | 295MB |
| **ResNet-17 (최종)** | **99.2%** | **95.7MB** ✅ |

---

## 👨‍👩‍👧‍👦 팀 소개 (Team F4)

<table>
  <tr>
    <td align="center">
      <img src="static/img/cate-img/sora.png" width="120"/><br/>
      <b>이소라</b><br/>
      웹 프론트·백엔드 개발<br/>
      Django, HTML/CSS, DB 설계, 배포
    </td>
    <td align="center">
      <img src="static/img/cate-img/youngjae.png" width="120"/><br/>
      <b>문영재</b><br/>
      AI 모델 개발<br/>
      전처리, 모델 최적화, 성능 분석
    </td>
    <td align="center">
      <img src="static/img/cate-img/dongmin.png" width="120"/><br/>
      <b>문동민</b><br/>
      AI 모델 개발<br/>
      ResNet 구조 설계, 경량화, 추론 구현
    </td>
  </tr>
</table>

---

## 🚀 향후 계획

- 다중 이미지 업로드 및 질병 비율 판단 기능 추가
- 드론 기반 대규모 작물 모니터링 이미지와 연계
- 작물 상태 이력 기반의 경고 시스템 개발

---

## 📎 참고 자료

- [AIHub 농작물 이미지](https://www.aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=data&dataSetSn=147)
- [ResNet 논문](https://arxiv.org/abs/1512.03385)
- [Template 출처 - Alazea](https://themewagon.com/themes/free-bootstrap-4-html5-plant-nursery-website-template-alazea/)
- 혁펜하임 유튜브, Tistory 블로그, Django 웹 개발 서적 등

---

“농업에 대한 관심이 늘어날수록, 우리는 더 나은 미래를 준비할 수 있습니다. F4는 그 시작을 돕고자 합니다.” 🌾

