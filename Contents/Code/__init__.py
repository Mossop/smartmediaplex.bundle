def Start():
    Plugin.AddViewGroup("Thumbs", viewMode="PosterList", mediaType="items", type=ViewType.Grid)

@handler("/photos/smartmedia", "Smart Media", thumb="smartmedia.png")
def Main():
    oc = ObjectContainer(title1="Smart Media", content=ContainerContent.Mixed)

    url = "%slist/roots" % (Prefs["url"])
    json = JSON.ObjectFromURL(url)
    for root in json:
        modelthumb=R("%s.png" % root["model"])
        oc.add(PhotoAlbumObject(
            key = Callback(Root, model=root["model"], title1=root["name"]),
            rating_key=root["model"], title=root["name"], thumb=modelthumb
        ))

    return oc

def ListFolder(title1, title2, model, url):
    oc = ObjectContainer(title1=title1, title2=title2, content=ContainerContent.Mixed)

    json = JSON.ObjectFromURL(url)
    for obj in json:
        if obj["model"] == "website.photo":
            imgurl = obj["fields"]["url"]
            thumburl = "%sphoto/%s/thumbnail/300" % (Prefs["url"], obj["pk"])
            oc.add(PhotoObject(
                key=imgurl, rating_key=imgurl, title=obj["fields"]["filename"], thumb=thumburl)
            )
        else:
            modelthumb=R("%s.png" % model)
            key="%s-%s" % (model, obj["pk"])
            oc.add(PhotoAlbumObject(
                key = Callback(Folder, model=model, id=obj["pk"], title1=title1, title2=obj["fields"]["name"]),
                rating_key=key, title=obj["fields"]["name"], thumb=modelthumb)
            )

    return oc

@route("/photos/smartmedia/root")
def Root(title1, model):
    return ListFolder(title1, None, model, "%s%s/contents" % (Prefs["url"], model))

@route("/photos/smartmedia/folder")
def Folder(title1, title2, model, id):
    return ListFolder(title1, title2, model, "%s%s/%s/contents" % (Prefs["url"], model, id))
