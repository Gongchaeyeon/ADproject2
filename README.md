# Kookmin Univ. 2020-2 AD project repository 공채연, 김선우

# 주제
한글 타자 디펜스 게임

# 필수 부분

0. 시작전에 난이도 설정
1. 단어장에서 단어를 랜덤으로뽑고
생성 위치도 랜덤하게 해서 핵으로 돌진!
2. 단어 박스 없애기 -> 입력 타자=단어
3. 단어박스랑 핵이 겹쳐짐 -> 라이프 하나 깎이고, 단어 소멸
4. 라이프 다 떨어지면 게임 끝남
5. 점수 올리기
6. 랭킹으로 나타내기
 --> 해결 
+. 한글로 했을 때 오류 해결 

# 게임적인 부분(보류)&추가기능
1. 배경 음악, 효과음



적들을 좀 다양하게 해야할 듯 
한방에, 두방에, 속도 2배 빠르게 

그리고 저글링 처럼 갉아 먹는 모션도 있음 좋겠음 

스테이지없이 만드는게 만들기는 편할듯?

# 일정

GUI 인터페이스(공채연) , 게임 부분 제작(김선우)
~11/7(토) 밤까지 깃헙에 푸쉬

두개를 머지하는 사람이(공채연,김선우)
회의 전까지 오류 등 발견해서 톡방에 올리기

다음 회의
11/11(수) 10시~

게임 구현 다 만드는 것은 3번째 주 까지 는 끝내고
그 이후에는 오류 수정, 테스트, 보고서 작성.

# simple ADS
-pyqt
점수 기록 데이터 베이스
Pyqt5 gui 클래스 – 시작화면, 종료화면
타자 입력 클래스

-Pygame 
단어 박스 클래스
핵 클래스
맵

# 추가 기능 -- 완료
1. game.py에서 그만두기 버튼 만들기 --> (저장하지 않고 나가기 OR 게임 계속 진행할 지 물어보기)
2. 배경음악, 단어들이 사라질 때 효과음
3. Gameover에서 점수 띄우고, 가운데 정렬 되도록
4. main.py에서 아이디 엔터 누르면 바로 실행되도록
5. 화면에서 Esc 누르면 창이 닫히도록
6. move 함수
# -------------------------------------------------
7. 가운데 원(지구) --> 단어들은 운석 느낌 -> 디자인 
  (가운데로 올수록 중력느낌으로 가속도 붙이기) (장점) --> 보고서에 작성.
8. 스피드 --> 임시로 level*(producedT에 대한 무리함수꼴)

(1~5) 공채연, (6~8) 김선우

# 해결하기
yes, no 클릭할 때 시간 멈추는 코드

# 디자인
지구-운석 (배경은 우주)
