def paging(request_page: int, row_cnt: int): # row_cnt = UserCrud(db).count_all_users()
    page_size = 10
    block_size = 10
    response_page = request_page - 1  # 넘겨받은 page번호를 인덱스 값으로 전환
    page_cnt_mok = row_cnt // page_size
    page_cnt_nmg = row_cnt % page_size
    page_cnt = page_cnt_mok if (page_cnt_nmg == 0) else page_cnt_mok + 1
    block_cnt_mok = page_cnt // page_size
    block_cnt_nmg = page_cnt % block_size
    block_cnt = block_cnt_mok if (block_cnt_nmg == 0) else block_cnt_mok + 1
    start_row_per_page = page_size * (response_page)
    response_block = (response_page) // block_size
    last_row_idx_per_total = row_cnt - 1
    last_row_idx_per_page = page_size - 1
    end_row_per_page = start_row_per_page + last_row_idx_per_page \
        if request_page != page_cnt \
        else last_row_idx_per_total
    start_page_per_block = response_block * block_size
    last_page_idx_per_total = page_cnt - 1
    last_block_idx_per_total = block_cnt - 1
    last_page_idx_per_block = block_size - 1
    end_page_per_block = start_page_per_block + last_page_idx_per_block \
        if response_block != last_block_idx_per_total \
        else last_page_idx_per_total
    prev_arrow = response_block != 0
    next_arrow = response_block != last_block_idx_per_total
    print("### 테스트 ### ")
    print(f"row_cnt ={row_cnt}")
    print(f"start_row_per_page ={start_row_per_page}")
    print(f"end_row_per_page ={end_row_per_page}")
    print(f"start_page_per_block ={start_page_per_block}")
    print(f"end_page_per_block ={end_page_per_block}")
    print(f"request_page={ request_page}")
    return {
        "row_cnt":row_cnt,
        "start_row_per_page":start_row_per_page,
        "end_row_per_page":end_row_per_page,
        "start_page_per_block":start_page_per_block,
        "end_page_per_block":end_page_per_block,
        "request_page":request_page,
        "prev_arrow":prev_arrow,
        "next_arrow":next_arrow
    }