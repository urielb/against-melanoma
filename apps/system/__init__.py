def GET_TREATMENT_PRICE():
    return models.Config.treatment_price()

def GET_TREATMENT_TIME_LIMIT():
    return models.Config.treatment_time_limit()

def GET_MIN_NUM_PHOTOS():
    return models.Config.min_num_photos()

def GET_FREE_TREATMENTS():
    return models.Config.free_treatments()