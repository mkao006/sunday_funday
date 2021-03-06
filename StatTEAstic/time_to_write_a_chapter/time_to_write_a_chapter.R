library(XML)
library(stringr)
library(magrittr)
library(ggplot2)

buildUrl = function(thread, page){
    paste0("http://ck101.com/thread-", thread, "-", page, "-1.html")
}

extractTimeStampsFromPage = function(url){
    failed = TRUE
    while(failed){
        doc = htmlTreeParse(url, useInternalNodes = T)
        if(!inherits(doc, "try-error"))
            failed = FALSE
    }   
    time_stamp_text =
        xpathSApply(doc, '//span[@class="postDateLine"]/text()', xmlValue)

    time_stamps_char =
        unlist(
            lapply(time_stamp_text, FUN = function(x){
                str_match(x, "[0-9]{4}\\-[0-9]+\\-[0-9]+.[0-9]{2}:[0-9]{2}")
            })
        )
    time_stamps = as.POSIXct(time_stamps_char, format = "%Y-%m-%d %H:%M")
    time_stamps
}




getMaxPageNumber = function(url){
    failed = TRUE
    while(failed){
        doc = try(htmlTreeParse(url, useInternalNodes = T))
        if(!inherits(doc, "try-error"))
            failed = FALSE
    }
    last_page =
        xpathSApply(doc, '//a[@class="last"]/text()', xmlValue)
    as.numeric(gsub("[^0-9]", "", last_page[1]))
}

extractNovelTimeStamps = function(thread){
    last_page = getMaxPageNumber(buildUrl(thread, "1"))
    lapply(1:last_page, FUN = function(x){
        current_page = buildUrl(thread, x)
        cat("Extracting page ", current_page, "\n")
        extractTimeStampsFromPage(current_page)
    }) %>%
        do.call("c", .)
}


calculate_hour_diff = function(time_stamps){
    diff(time_stamps)/60/60
}




da_zhu_zai_time_stamp = extractNovelTimeStamps("2762483")
da_zhu_zai_time_diff = calculate_hour_diff(da_zhu_zai_time_stamp)
da_zhu_zai_time_diff = da_zhu_zai_time_diff[da_zhu_zai_time_diff < 168]

do_puo_time_stamp = extractNovelTimeStamps("1455308")
do_puo_time_diff = calculate_hour_diff(do_puo_time_stamp)
do_puo_time_diff = do_puo_time_diff[do_puo_time_diff < 168 & do_puo_time_diff > 1]

wu_dong_time_stamp = extractNovelTimeStamps("1979168")
wu_dong_time_diff = calculate_hour_diff(wu_dong_time_stamp)
wu_dong_time_diff = wu_dong_time_diff[wu_dong_time_diff < 168]



full_time_diff = c(do_puo_time_diff, wu_dong_time_diff, da_zhu_zai_time_diff)

novel_time =
    data.frame(duration = full_time_diff,
               post = c(c(1:length(do_puo_time_diff)),
                         c(1:length(wu_dong_time_diff)),
                         c(1:length(da_zhu_zai_time_diff))),
               novel = c(rep("1.do_puo", length(do_puo_time_diff)),
                         rep("2.wu_dong", length(wu_dong_time_diff)),
                         rep("3.da_zhu_zai", length(da_zhu_zai_time_diff))))
           

ggplot(data = novel_time, aes(x = post, y = duration)) +
    geom_line() +
    geom_smooth(col = "red", level = 0.99) + 
    facet_wrap(~novel)


with(novel_time, tapply(duration, novel, summary))
