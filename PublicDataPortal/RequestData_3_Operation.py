import  requests                                # REST API 호출
from    bs4         import  BeautifulSoup       # XML 데이터 해석
import  csv                                     # .csv 파일로 저장
import  time                                    # 실행시간 측정
import  math                                    # 반올림; .floor(), .ceil()
import  os                                      # 파일명 중복 체크


# bs4Test : params에 최초 설정된 대로 xml 다운로드 테스트
def bs4Test(url, params, run = True) :
    if run :
        response = requests.get(url, params=params)                                         # . get() 자체적으로 encoding을 하므로 decoding key를 사용
        soup = BeautifulSoup(response.content, "html.parser")                               # 'b 삭제, 행갈이 추가
        print("soup\t\t\t:\n", soup)                                                        # 테스트 출력


def Operation(
    url,
    page,
    path,
    sleepTime,
    params,
    columns,
    test = False
    ) :

    # 총 페이지 수
    totalPage = int((page['end'] - page['start'])/page['interval']) + 1

    # 저장 경로 & 파일명 설정
    savePath = path['path'] + '/' + path['fileName'] + '_' + str(page['start']) + "_" + str(page['end']) + ".csv"

    # columns → "item.****.text"꼴로 변환 (xml 문서 분석용)
    soupColumns = []
    for c in columns :
        soupColumns.append("item." + c.lower() + ".text")

    # 다운로드 개시 전 테스트
    if test :
        print("<테스트 모드>")    
        print("totalPage\t\t:", totalPage)
        print("savePath\t\t:", savePath)
        print("soupColumns (Top 5)\t:", soupColumns[0:5])
        bs4Test(url, params, False)                                                         # bs4Test : params에 최초 설정된 대로 xml 다운로드 테스트, (run = False : 실행 X)

    # 다운로드
    obs = 1
    # startTime = time.perf_counter()                                                       # 시작 시간

    with open(savePath, 'a', newline='') as f:                                              # f: 띄어쓰면 오류

        wr = csv.writer(f)

        if os.path.getsize(savePath) > 0 :                                                  # 실행 전 파일명 중복 여부 검사
            print("이미 존재하는 파일에 이어씁니다. (", savePath, ")")
        else :
            wr.writerow(columns)                                                            # 최초 작성시 1행에 헤더 라인 삽입 (변수명)

        for i in range(page['start'], page['end'] + 1, page['interval']) :

            if test :
                print(i)

            params['pageNo'] = i
            response = requests.get(url, params=params)                                     # . get() 자체적으로 encoding을 하므로 decoding key를 사용
            soup = BeautifulSoup(response.content, "html.parser")                           # 'b 삭제, 행갈이 추가

            # Stack data into pandas data frame (on memory)
            for item in soup.findAll("response") :                                          # 모든 데이터는 <body> </body> 태그 사이에 위치
                temp = []
                for j in range(0, len(soupColumns)) :
                    if eval(soupColumns[j]) != None :                                       # 각 데이터 열(태그) 존재 여부 확인
                        temp.append(eval(soupColumns[j]))                                   # eval() : "item.numofrows.text" to item.numofrows.text
                    else :
                        temp.append("")                                                     # 빈 태그에 "" 삽입
                if test :
                    print(temp)                                                             # test
                wr.writerow(temp)



# 2.2에서 아직 이식하지 못 한 코드
def temp() :

    # 2.2.1 Background operation related with 2.2 Setting

    # Find where the startPage and endPage are
    startPage = math.floor(startRow / int(params['numOfRows']))                                 # floor() : rounding down
    endPage = math.ceil(endRow / int(params['numOfRows']))                                      # ceil() : rounding up
    totalPage = endPage - startPage + 1
    measurePerfTerm = max(1, totalPage / 10)                                                    # check the completion ratio 10 times 


    # 2.3 Loop to request data continously

    print("데이터 다운로드를 시작합니다.")
    startTime = time.perf_counter()                                                             # set the reference point to measure performance
    
    for i in range(startPage, endPage + 1) :                                                    # endPage + 1 → run until endPage

        # print(i)                                                                              # test : ok

        # Measure the completion ratio and avoid the data request frequency limmit if it exists (180 sec.)
        if (i != startPage) and (i % measurePerfTerm == 0 or i == endPage)  :
            elapseTime = time.perf_counter() - startTime
            completionRatio = (i - startPage + 1) / totalPage
            print("{:0,.1f}분 남았습니다. (진행률 : {:0,.1f}%)".format((elapseTime / completionRatio - elapseTime) / 60, completionRatio * 100))
            # time.sleep(sleepTime)


    # 2.4 Loop to request missing data 

    missingPage = (endPage - startPage + 1) - len(df)                                           # get the number of missing data
    measurePerfTerm = max(1, totalPage / 10)                                                    # check the completion ratio 10 times
    if missingPage == 0 :
        print("누락된 데이터가 없습니다.")
    else :
        print("누락된 데이터({}건)의 추가 다운로드를 시작합니다.".format(missingPage))


    # 2.5 Save data as a .csv fie

    # print(df)                                                                                 # test : ok
    if os.path.isfile(path) :                                                                   # to prevent overwriting the file
        print("이미 같은 이름의 파일이 존재합니다. (", path, ")")
        # don't need to run the loop again, just change the old file's name
    else :
        df.to_csv(path, encoding = 'utf-8-sig')
        if os.path.isfile(path) :                                                               # I am too hospitable, you must have won a man like the lotto!
            print("데이터가 정상적으로 저장되었습니다. (", path, ")")
        else :
            print("데이터가 정상적으로 저장되지 않았습니다.")



if __name__ == "__main__" :

    import RequestData_3_Run as Run

    Operation(
        Run.url,
        Run.page,
        Run.path,
        Run.sleepTime,
        Run.params,
        Run.columns,
        test = True
    )