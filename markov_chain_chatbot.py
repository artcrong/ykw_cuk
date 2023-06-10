import pandas as pd
from collections import defaultdict
from konlpy.tag import Okt

# 형태소 분석기 초기화
tokenizer = Okt()

# 마르코프 체인 차수 2
order = 2

# CSV 파일을 판다스 데이터프레임 타입으로 변경
df = pd.read_csv("ChatbotData.csv", encoding='utf-8')

# 함수 매개변수 : 입력된 문장, 마르코프 체인 차수
def find_best_answer(input_sentence, order):
    # 적절한 응답문에 대한 답변문장의 Index(Key 값), 유사도(Value 값)의 초기화
    input_sentence_result = defaultdict(int)

    ### 과제 상세 설명 1. 학습데이터의 질문과 chat의 질문의 유사도를 레벤슈타인 거리를 이용해 구하기
    for index, sentences in enumerate(df['Q']):
        
        # 챗봇데이터에 대한 마르코프 체인 적용
        morphemes = tokenizer.morphs(sentences)
        words = [morpheme for morpheme in morphemes if morpheme not in ['!', '?', '~', ',', '.', ';', '.,', '?,', '!,']] 
        #print(index, words)

        # 입력 문장에 대한 마르코프 체인 적용
        input_sentences = tokenizer.morphs(input_sentence)
        input_sentences_words = [s for s in input_sentences if s not in ['!', '?', '~', ',', '.', ';', '.,', '?,', '!,']]

        # 유사도에 따라 1 증가
        for i in range(len(input_sentences_words) - order):
            for j in range(len(words) - order):
                if input_sentences_words[i:i+order] == words[j:j+order]:
                    input_sentence_result[index] += 1

    ### 과제 상세 설명 2. chat의 질문과 레벤슈타인 거리와 가장 유사한 학습데이터의 질문의 인덱스를 구하기 ###
    # 유사도가 최대값인 문장의 인덱스를 반환
    max_sentence = max(input_sentence_result, key=input_sentence_result.get)
    #print(input_sentence_result)

    return max_sentence

while True:
    # 문장 입력 받기
    input_sentence = input("Input Sentence : ")

    # '종료'를 입력하면 프로그램 종료
    if input_sentence.lower() == '종료':
        break

    # 적합한 문장의 인덱스를 구하는 함수
    answer = find_best_answer(input_sentence, order)

    ### 과제 상세 설명 3. 학습데이터의 인덱스의 답을 chat의 답변을 채택한 뒤 출력 ###
    print("Answer :", df.loc[answer][1])
    #print(df.loc[max_sentence])

### 실행 예
# ----------------------------------
# Input Sentence : 바다 보러 가자
# Answer : 바다는 사계절 내내 좋아요.
# ----------------------------------
# Input Sentence : 비행기 타러 간다
# Answer : 잘 다녀오세요.
# ----------------------------------
# Input Sentence : 종료
