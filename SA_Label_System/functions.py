


def get_image_score(score_list):
    frequency = [0,0,0,0,0,0]
    mode_num = 0
    mode_score = -1
    sum_score = 0
    cnt = 0
    for score in score_list:
        cnt += 1
        sum_score += score
        frequency[int(score)] += 1
        if frequency[int(score)]>mode_num:
            mode_num = frequency[int(score)]
            mode_score = score
    if mode_num==1:
        if cnt==0:
            return -1
        return int(sum_score/cnt)
    else:
        return mode_score
