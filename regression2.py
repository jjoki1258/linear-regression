import pandas as pd
fish=pd.read_csv('https://bit.ly/fish_csv_data')
fish.head()  #데이터 받기-처음 5행만 출력

print(pd.unique(fish['Species'])) #species 열을 타깃으로 만들고 나머지 5개열은 입력 데이터로 사용

fish_input=fish[['Weight','Length','Diagonal','Height','Width']].to_numpy() #input 5 class

print(fish_input[:5])

fish_target=fish['Species'].to_numpy()

from sklearn.model_selection import train_test_split #train test나눔
train_input, test_input, train_target, test_target = train_test_split(fish_input,fish_target, random_state=42)

from sklearn.preprocessing import StandardScaler #표준화 삼입 - 데이터전처리

ss= StandardScaler()

ss.fit(train_input)
train_scaled=ss.transform(train_input)
test_scaled=ss.transform(test_input)

from sklearn.neighbors import KNeighborsClassifier #k최근접 이웃 분류기의 확률예측

kn=KNeighborsClassifier(n_neighbors=3)#이웃 3개로 결정

kn.fit(train_scaled, train_target)

print(kn.score(train_scaled, train_target))

print(kn.score(test_scaled,test_target))

print(kn.classes_)

print(kn.predict(test_scaled[:5]))

import numpy as np  #class 속성 확률
proba=kn.predict_proba(test_scaled[:5])# 테스트 스케일 5까지
print(np.round(proba,decimals=4)) #소수점 4번째자리까지 표현

distances,indexes = kn.kneighbors(test_scaled[3:4]) #클래스확률 예측
print(train_target[indexes]) #최근접 이웃의 클래스 확인

import numpy as np

import matplotlib.pyplot as plt

z=np.arange(-5,5,0.1)

phi=1/(1+np.exp(-z)) #시그모이드 함수 확률(0~1)

plt.plot(z,phi)

plt.xlabel('z')
plt.ylabel('phi')
plt.show() #0.5보다 크면 양성클래스, 0.5보다 작으면 음성클래스

char_arr=np.array(['A','B','C','D','E']) #불리언 언덱싱 -> true, false 값을 전달하여 행 선택
print(char_arr[True,False,True,False,False]) # output값을 입력 후 변동

bream_smelt_indexes=(train_target == 'Bream') | (train_target == 'Smelt') #도미와 빙어일경우 true ,그 외는 모두 false
train_bream_smelt=train_scaled[bream_smelt_indexes]
target_bream_smelt=train_target[bream_smelt_indexes]

from sklearn.linear_model import LogisticRegression

lr= LogisticRegression()

lr.fit(train_bream_smelt,target_bream_smelt) #샘플 훈련

print(lr.predict(train_bream_smelt[:5]))
print(lr.predict_proba(train_bream_smelt[:5])) #처음 5개 샘플 예측 확률 ->첫번쨰 음성클래스 일 확률, 두번째 양성클래스일 확률

print(lr.classes_)#선형회귀 class 도입

print(lr.coef_,lr.intercept_) #로지스틱회귀모델이 학습한 방정식은 다음과 같다



decisions=lr.decision_function(train_bream_smelt[:5]) #로지스틱 회귀
print(decisions) #로지스틱 회귀모델로 z값 계산

from scipy.special import expit
print(expit(decisions))

#다중분류 실시
lr=LogisticRegression(C=20, max_iter=1000) #로지스틱 선형회귀 c=20(규제변수)릿지방식, max_tier=1000(반복횟수)
lr.fit(train_scaled, train_target)
print(lr.score(train_scaled,train_target))
print(lr.score(test_scaled,test_target))

print(lr.predict(test_scaled[:5]))
print(np.round(proba,decimals=3)) #proba=3 , 설정, 소수점 3자리까지만

print(lr.classes_) #선형회귀 모델 출력

print(lr.coef_.shape,lr.intercept_.shape) #열5 행7-> z를 7번계산

decision = lr.decision_function(test_scaled[:5]) # 시그모이드 함수에 통과시키면 확률 얻을수 있음
print(np.round(decision,decimals=2))

from scipy.special import softmax  #소프트맥스 축 3으로 전달  (다중분류일경우 시그모이드 함수가 아니라 소프트맥수 함수 사용 )
proba=softmax(decision,axis=1)
print(np.round(proba,decimals=3))