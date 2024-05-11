from yt_dlp import YoutubeDL

def get_info(link):
    x = YoutubeDL()

    try: 
        formats = x.extract_info(link, download=False)
    except:
        return

    info_lst = [formats['title'], formats['thumbnail']]

    formats = formats.get("formats", [])

    dic_aud = {}
    dic_vid = {}

    for format in formats:
        if "filesize" in format:
            #if format["filesize"]:
                if str(format['abr']) != '0' and format['abr'] and format["ext"] == "m4a":
                    dic_aud[format['format_id']] = {"Size":str(format["filesize"]), "Extension":str(format["ext"]),"Bitrate":str(format['abr'])}
                elif (format["ext"] == "mp4" or format["ext"] == "webm") and format["acodec"] != "none" and format["height"] != None:
                    dic_vid[format['format_id']] = {"Size":str(format["filesize"]), "Extension":str(format["ext"]),"fps":str(format['fps']),"Quality":str(format["height"])}

    print(dic_vid)
    newDic_vid = {}
    tmp1 = None; tmp2 = None
    for i,j in dic_vid.items():
        if tmp1 == None:
            tmp1 = i
            tmp2 = j
        else:
            if tmp2["Quality"] != j["Quality"]:
                newDic_vid.update({tmp1:tmp2})
                tmp1 = i
                tmp2 = j
            else:
                tmp1 = i
                tmp2 = j
                
    newDic_vid.update({tmp1:tmp2})
    
    return info_lst, dic_aud, newDic_vid

def sizeof_fmt(num, suffix='B'):
    for unit in ['', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB']:
        if abs(num) < 1024.0:
            return f"{num:.1f} {unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f} Yi{suffix}"


