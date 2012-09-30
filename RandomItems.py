# *  Thanks to:
# *
# *  Nuka for the original RecentlyAdded.py on which this is based
# *
# *  ppic, Hitcher,ronie & phil65, Martijn for the updates

import xbmc
import xbmcgui
import xbmcaddon
import sys
import os
import random

if sys.version_info < (2, 7):
    import simplejson
else:
    import json as simplejson

__addon__        = xbmcaddon.Addon()
__addonid__      = __addon__.getAddonInfo('id')
__addonversion__ = __addon__.getAddonInfo('version')

def log(txt):
    message = '%s: %s' % (__addonid__, txt)
    xbmc.log(msg=message, level=xbmc.LOGDEBUG)

class Main:
    # grab the home window
    WINDOW = xbmcgui.Window( 10000 )

    def _clear_properties( self ):
        # reset totals property for visible condition
        self.WINDOW.clearProperty( "RandomMovie.Count" )
        self.WINDOW.clearProperty( "RandomEpisode.Count" )
        self.WINDOW.clearProperty( "RandomMusicVideo.Count" )
        self.WINDOW.clearProperty( "RandomSong.Count" )
        self.WINDOW.clearProperty( "RandomAlbum.Count" )
        self.WINDOW.clearProperty( "RandomAddon.Count" )
        # we clear title for visible condition
        for count in range( self.LIMIT ):
            self.WINDOW.clearProperty( "RandomMovie.%d.Title"      % ( count + 1 ) )
            self.WINDOW.clearProperty( "RandomEpisode.%d.Title"    % ( count + 1 ) )
            self.WINDOW.clearProperty( "RandomMusicVideo.%d.Title" % ( count + 1 ) )
            self.WINDOW.clearProperty( "RandomSong.%d.Title"       % ( count + 1 ) )
            self.WINDOW.clearProperty( "RandomAlbum.%d.Title"      % ( count + 1 ) )
            self.WINDOW.clearProperty( "RandomAddon.%d.Name"       % ( count + 1 ) )

    def _parse_argv( self ):
        try:
            # parse sys.argv for params
            params = dict( arg.split( "=" ) for arg in sys.argv[ 1 ].split( "&" ) )
        except:
            # no params passed
            params = {}
        # set our preferences
        self.LIMIT = int( params.get( "limit", "5" ) )
        self.UNPLAYED = params.get( "unplayed", "False" )
        self.PLAY_TRAILER = params.get( "trailer", "False" )
        self.ALARM = int( params.get( "alarm", "0" ) )
        self.ALBUMID = params.get( "albumid", "" )

    def _set_alarm( self ):
        # only run if user/skinner preference
        if ( not self.ALARM ): return
        # set the alarms command
        command = "XBMC.RunScript(%s,limit=%d&unplayed=%s&trailer=%s&alarm=%d)" % ( __addonid__, self.LIMIT, str( self.UNPLAYED ), str( self.PLAY_TRAILER ), self.ALARM, )
        xbmc.executebuiltin( "AlarmClock(RandomItems,%s,%d,true)" % ( command, self.ALARM, ) )

    def __init__( self ):
        # parse argv for any preferences
        self._parse_argv()
        # check if we were executed internally
        if self.ALBUMID:
            xbmc.executeJSONRPC('{ "jsonrpc": "2.0", "method": "Player.Open", "params": { "item": { "albumid": %d } }, "id": 1 }' % int(self.ALBUMID))
        else:
            # clear properties
            self._clear_properties()
            # set any alarm
            self._set_alarm()
            # fetch media info
            self._fetch_movie_info()
            self._fetch_episode_info()
            self._fetch_musicvideo_info()
            self._fetch_album_info()
            self._fetch_artist_info()
            self._fetch_song_info()
            self._fetch_addon_info()

    def _fetch_movie_info( self ):
        if self.UNPLAYED == "True":
            json_query = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": {"properties": ["title", "playcount", "year", "plot", "runtime", "fanart", "thumbnail", "file", "trailer", "rating"], "filter": {"field": "playcount", "operator": "lessthan", "value": "1"}, "sort": {"method": "random" }, "limits": {"end": %d} }, "id": 1}' %self.LIMIT)
        else:
            json_query = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": {"properties": ["title", "playcount", "year", "plot", "runtime", "fanart", "thumbnail", "file", "trailer", "rating"], "sort": {"method": "random" }, "limits": {"end": %d} }, "id": 1}' %self.LIMIT)
        json_query = unicode(json_query, 'utf-8', errors='ignore')
        # separate the records
        json_response = simplejson.loads(json_query)
        if json_response.has_key('result') and json_response['result'] != None and json_response['result'].has_key('movies'):
            count = 0
            total = str(len(json_response))
            for item in json_response['result']['movies']:
                count += 1
                # set our properties
                self.WINDOW.setProperty( "RandomMovie.%d.Title"       % ( count ), item['title'] )
                self.WINDOW.setProperty( "RandomMovie.%d.Rating"      % ( count ), str(round(float(item['rating']),1)) )
                self.WINDOW.setProperty( "RandomMovie.%d.Year"        % ( count ), str(item['year']))
                self.WINDOW.setProperty( "RandomMovie.%d.Plot"        % ( count ), item['plot'] )
                self.WINDOW.setProperty( "RandomMovie.%d.RunningTime" % ( count ), item['runtime'] )
                self.WINDOW.setProperty( "RandomMovie.%d.Path"        % ( count ), item['file'] )
                self.WINDOW.setProperty( "RandomMovie.%d.Trailer"     % ( count ), item['trailer'] )
                self.WINDOW.setProperty( "RandomMovie.%d.Fanart"      % ( count ), item['fanart'] )
                self.WINDOW.setProperty( "RandomMovie.%d.Thumb"       % ( count ), item['thumbnail'] )
                self.WINDOW.setProperty( "RandomMovie.Count"          , total )

    def _fetch_episode_info( self ):
        if self.UNPLAYED == "True":
            json_query = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodes", "params": { "properties": ["title", "playcount", "season", "episode", "showtitle", "plot", "fanart", "thumbnail", "file", "rating"], "filter": {"field": "playcount", "operator": "lessthan", "value": "1"}, "sort": {"method": "random" }, "limits": {"end": %d} }, "id": 1}' %self.LIMIT)
        else:
            json_query = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodes", "params": { "properties": ["title", "playcount", "season", "episode", "showtitle", "plot", "fanart", "thumbnail", "file", "rating"], "sort": {"method": "random" }, "limits": {"end": %d} }, "id": 1}' %self.LIMIT)
        json_response = unicode(json_query, 'utf-8', errors='ignore')
        jsonobject = simplejson.loads(json_response)
        if jsonobject.has_key('result') and jsonobject['result'] != None and jsonobject['result'].has_key('episodes'):
            count = 0
            total = str( len( json_response ) )
            for item in jsonobject['result']['episodes']:
                count += 1
                season = "%.2d" % float(item['season'])
                episode = "%.2d" % float(item['episode'])
                episodeno = "s%se%s" % ( season,  episode, )
                # set our properties
                self.WINDOW.setProperty( "RandomEpisode.%d.ShowTitle"     % ( count ), item['showtitle'] )
                self.WINDOW.setProperty( "RandomEpisode.%d.EpisodeTitle"  % ( count ), item['title'] )
                self.WINDOW.setProperty( "RandomEpisode.%d.EpisodeNo"     % ( count ), episodeno )
                self.WINDOW.setProperty( "RandomEpisode.%d.EpisodeSeason" % ( count ), season )
                self.WINDOW.setProperty( "RandomEpisode.%d.EpisodeNumber" % ( count ), episode )
                self.WINDOW.setProperty( "RandomEpisode.%d.Rating"        % ( count ), str(round(float(item['rating']),1)) )
                self.WINDOW.setProperty( "RandomEpisode.%d.Plot"          % ( count ), item['plot'] )
                self.WINDOW.setProperty( "RandomEpisode.%d.Path"          % ( count ), item['file'] )
                self.WINDOW.setProperty( "RandomEpisode.%d.Fanart"        % ( count ), item['fanart'] )
                self.WINDOW.setProperty( "RandomEpisode.%d.Thumb"         % ( count ), item['thumbnail'] )
                self.WINDOW.setProperty( "RandomEpisode.Count"            , total )

    def _fetch_musicvideo_info( self ):
        if self.UNPLAYED == "True":
            json_query = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMusicVideos", "params": {"properties": ["title", "artist", "playcount", "year", "plot", "runtime", "fanart", "thumbnail", "file"], "filter": {"field": "playcount", "operator": "lessthan", "value": "1"}, "sort": {"method": "random"}, "limits": {"end": %d}}, "id": 1}'  %self.LIMIT)
        else:
            json_query = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMusicVideos", "params": {"properties": ["title", "artist", "playcount", "year", "plot", "runtime", "fanart", "thumbnail", "file"], "sort": {"method": "random"}, "limits": {"end": %d}}, "id": 1}'  %self.LIMIT)
        json_query = unicode(json_query, 'utf-8', errors='ignore')
        # separate the records
        json_response = simplejson.loads(json_query)
        if json_response.has_key('result') and json_response['result'] != None and json_response['result'].has_key('musicvideos'):
            count = 0
            total = str(len(json_response))
            for item in json_response['result']['musicvideos']:
                count += 1
                # set our properties
                self.WINDOW.setProperty( "RandomMusicVideo.%d.Title"       % ( count ), item['title'] )
                self.WINDOW.setProperty( "RandomMusicVideo.%d.Year"        % ( count ), str(item['year']))
                self.WINDOW.setProperty( "RandomMusicVideo.%d.Plot"        % ( count ), item['plot'] )
                self.WINDOW.setProperty( "RandomMusicVideo.%d.RunningTime" % ( count ), item['runtime'] )
                self.WINDOW.setProperty( "RandomMusicVideo.%d.Path"        % ( count ), item['file'] )
                self.WINDOW.setProperty( "RandomMusicVideo.%d.Fanart"      % ( count ), item['fanart'] )
                self.WINDOW.setProperty( "RandomMusicVideo.%d.Artist"      % ( count ), " / ".join( item['artist'] ) )
                self.WINDOW.setProperty( "RandomMusicVideo.%d.Thumb"       % ( count ), item['thumbnail'] )
                self.WINDOW.setProperty( "RandomMusicVideo.Count"          , total )

    def _fetch_album_info( self ):
        if self.UNPLAYED == "True":
            json_query = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "AudioLibrary.GetAlbums", "params": {"properties": ["title", "description", "albumlabel", "artist", "genre", "year", "thumbnail", "fanart", "rating", "playcount"], "filter": {"field": "playcount", "operator": "lessthan", "value": "1"}, "sort": {"method": "random"}, "limits": {"end": %d}}, "id": 1}'  %self.LIMIT)
        else:
            json_query = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "AudioLibrary.GetAlbums", "params": {"properties": ["title", "description", "albumlabel", "artist", "genre", "year", "thumbnail", "fanart", "rating", "playcount"], "sort": {"method": "random"}, "limits": {"end": %d}}, "id": 1}'  %self.LIMIT)
        json_response = unicode(json_query, 'utf-8', errors='ignore')
        jsonobject = simplejson.loads(json_response)
        if jsonobject.has_key('result') and jsonobject['result'] != None and jsonobject['result'].has_key('albums'):
            count = 0
            total = str(len(jsonobject))
            for item in jsonobject['result']['albums']:
                count += 1
                rating = str(item['rating'])
                if rating == '48':
                    rating = ''
                path = 'XBMC.RunScript(' + __addonid__ + ',albumid=' + str(item['albumid']) + ')'
                self.WINDOW.setProperty( "RandomAlbum.%d.Title"  % ( count ), item['title'] )
                self.WINDOW.setProperty( "RandomAlbum.%d.Rating" % ( count ), rating )
                self.WINDOW.setProperty( "RandomAlbum.%d.Year"   % ( count ), str(item['year']) )
                self.WINDOW.setProperty( "RandomAlbum.%d.Artist" % ( count ), " / ".join(item['artist']) )
                self.WINDOW.setProperty( "RandomAlbum.%d.Path"   % ( count ), path )
                self.WINDOW.setProperty( "RandomAlbum.%d.Fanart" % ( count ), item['fanart'] )
                self.WINDOW.setProperty( "RandomAlbum.%d.Thumb"  % ( count ), item['thumbnail'] )
                self.WINDOW.setProperty( "RandomAlbum.%d.Album_Description"  % ( count ), item['description'] )
                self.WINDOW.setProperty( "RandomAlbum.Count"     , total )

    def _fetch_artist_info( self ):
        json_query = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "AudioLibrary.GetArtists", "params": {"properties": ["genre", "description", "fanart", "thumbnail"], "sort": {"method": "random"}, "limits": {"end": %d}}, "id": 1}'  %self.LIMIT)
        json_response = unicode(json_query, 'utf-8', errors='ignore')
        jsonobject = simplejson.loads(json_response)
        if jsonobject.has_key('result') and jsonobject['result'] != None and jsonobject['result'].has_key('artists'):
            count = 0
            total = str(len(jsonobject))
            for item in jsonobject['result']['artists']:
                count += 1
                path = 'musicdb://2/' + str(item['artistid']) + '/'
                self.WINDOW.setProperty( "RandomArtist.%d.Title"  % ( count ), item['label'] )
                self.WINDOW.setProperty( "RandomArtist.%d.Genre" % ( count ), " / ".join( item['genre'] ) )
                self.WINDOW.setProperty( "RandomArtist.%d.Path"   % ( count ), path )
                self.WINDOW.setProperty( "RandomArtist.%d.Fanart" % ( count ), item['fanart'] )
                self.WINDOW.setProperty( "RandomArtist.%d.Thumb"  % ( count ), item['thumbnail'] )
                self.WINDOW.setProperty( "RandomArtist.%d.Artist_Description"  % ( count ), item['description'] )
                self.WINDOW.setProperty( "RandomArtist.Count"     , total )

    def _fetch_song_info( self ):
        if self.UNPLAYED == "True":
            json_query = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "AudioLibrary.GetSongs", "params": {"properties": ["title", "playcount", "artist", "album", "year", "file", "thumbnail", "fanart", "rating"], "filter": {"field": "playcount", "operator": "lessthan", "value": "1"}, "sort": {"method": "random"}, "limits": {"end": %d}}, "id": 1}'  %self.LIMIT)
        else:
            json_query = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "AudioLibrary.GetSongs", "params": {"properties": ["title", "playcount", "artist", "album", "year", "file", "thumbnail", "fanart", "rating"], "sort": {"method": "random"}, "limits": {"end": %d}}, "id": 1}'  %self.LIMIT)
        json_response = unicode(json_query, 'utf-8', errors='ignore')
        jsonobject = simplejson.loads(json_response)
        if jsonobject.has_key('result') and jsonobject['result'] != None and jsonobject['result'].has_key('songs'):
            count = 0
            total = str( len( jsonobject ) )
            for item in jsonobject['result']['songs']:
                count += 1
                self.WINDOW.setProperty( "RandomSong.%d.Title"  % ( count ), item['title'] )
                self.WINDOW.setProperty( "RandomSong.%d.Rating" % ( count ), str(int(item['rating'])-48) )
                self.WINDOW.setProperty( "RandomSong.%d.Year"   % ( count ), str(item['year']) )
                self.WINDOW.setProperty( "RandomSong.%d.Artist" % ( count ), " / ".join( item['artist'] ) )
                self.WINDOW.setProperty( "RandomSong.%d.Album"  % ( count ), item['album'] )
                self.WINDOW.setProperty( "RandomSong.%d.Path"   % ( count ), item['file'] )
                self.WINDOW.setProperty( "RandomSong.%d.Fanart" % ( count ), item['fanart'] )
                self.WINDOW.setProperty( "RandomSong.%d.Thumb"  % ( count ), item['thumbnail'] )
                self.WINDOW.setProperty( "RandomSong.Count"     , total )

    def _fetch_addon_info( self ):
        json_query = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Addons.GetAddons", "params": {"properties": ["name", "author", "summary", "version", "fanart", "thumbnail"]}, "id": 1}')
        json_response = unicode(json_query, 'utf-8', errors='ignore')
        jsonobject = simplejson.loads(json_response)
        if jsonobject.has_key('result') and jsonobject['result'] != None and jsonobject['result'].has_key('addons'):
            total = str( len( jsonobject ) )
            # find plugins and scripts
            addonlist = []
            for item in jsonobject['result']['addons']:
                if item['type'] == 'xbmc.python.script' or item['type'] == 'xbmc.python.pluginsource':
                    addonlist.append(item)
            # randomize the list
            random.shuffle(addonlist)
            count = 0
            for item in addonlist:
                count += 1
                self.WINDOW.setProperty( "RandomAddon.%d.Name"    % ( count ), item['name'] )
                self.WINDOW.setProperty( "RandomAddon.%d.Author"  % ( count ), item['author'] )
                self.WINDOW.setProperty( "RandomAddon.%d.Summary" % ( count ), item['summary'] )
                self.WINDOW.setProperty( "RandomAddon.%d.Version" % ( count ), item['version'] )
                self.WINDOW.setProperty( "RandomAddon.%d.Path"    % ( count ), item['addonid'] )
                self.WINDOW.setProperty( "RandomAddon.%d.Fanart"  % ( count ), item['fanart'] )
                self.WINDOW.setProperty( "RandomAddon.%d.Thumb"   % ( count ), item['thumbnail'] )
                self.WINDOW.setProperty( "RandomAddon.%d.Type"    % ( count ), item['type'] )
                self.WINDOW.setProperty( "RandomAddon.Count"      , total )
                # stop if we've reached the number of items we need
                if count == self.LIMIT:
                    break

if ( __name__ == "__main__" ):
        log('script version %s started' % __addonversion__)
        Main()
log('script stopped')
