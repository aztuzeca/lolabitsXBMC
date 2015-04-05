# -*- coding: utf-8 -*-

""" lolabits.es
    2015 fightnight fork - edit aztuzeca"""

import xbmc,xbmcaddon,xbmcgui,xbmcplugin,urllib,urllib2,os,re,sys,datetime,time
from t0mm0.common.net import Net
net=Net()

####################################################### CONSTANTES #####################################################

version = '1.0.1'
addon_id = 'plugin.video.lolabits'
MainURL = 'http://lolabits.es/'
art = '/resources/art/'
user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36'
selfAddon = xbmcaddon.Addon(id=addon_id)
wtpath = selfAddon.getAddonInfo('path').decode('utf-8')
iconpequeno=wtpath + art + 'iconpq.jpg'
traducaoma= selfAddon.getLocalizedString
mensagemok = xbmcgui.Dialog().ok
mensagemprogresso = xbmcgui.DialogProgress()
downloadPath = selfAddon.getSetting('download-folder').decode('utf-8')
pastaperfil = xbmc.translatePath(selfAddon.getAddonInfo('profile')).decode('utf-8')
cookies = os.path.join(pastaperfil, "cookies.lwp")
username_lb = urllib.quote(selfAddon.getSetting('lolabits-username'))

####
if selfAddon.getSetting('lolabits-enable') == 'true' and selfAddon.getSetting('lolabits-check') == 'true': status_lolabits=True
else: status_lolabits=False
####

def traducao(texto):
      return traducaoma(texto).encode('utf-8')

#################################################### LOGIN LOLABITS #####################################################

def login_lolabits(defora=False):
      print "Sin cookie. A iniciar login"
      try:
            link=abrir_url(MainURL)
            token=re.compile('<input name="__RequestVerificationToken" type="hidden" value="(.+?)" />').findall(link)[0]
            
            
            form_d = {'RedirectUrl':'','Redirect':'True','FileId':0,'Login':username_lb,'Password':selfAddon.getSetting('lolabits-password'),'RememberMe':'true','__RequestVerificationToken':token}
            ref_data = {'Accept': '*/*', 'Content-Type': 'application/x-www-form-urlencoded','Origin': 'http://lolabits.es', 'X-Requested-With': 'XMLHttpRequest', 'Referer': 'http://lolabits.es/','User-Agent':user_agent}
            endlogin=MainURL + 'action/login/login'
            try:
                  logintest= net.http_POST(endlogin,form_data=form_d,headers=ref_data).content.encode('latin-1','ignore')
            except: logintest='Erro'
      except:
            link='Erro'
            logintest='Erro'

      if re.search('003eA senha indicada n',logintest):
            mensagemok('Lolabits.es',traducao(40002))
            entrarnovamente(1)
            return False
      elif re.search('existe. Certifica-te que indicaste o nome correcto.',logintest):
            mensagemok('Lolabits.es',traducao(40003))
            entrarnovamente(1)
            return False
      elif re.search(username_lb,logintest):
            #xbmc.executebuiltin("XBMC.Notification(abelhas.pt,"+traducao(40004)+",'500000',"+iconpequeno.encode('utf-8')+")")
            net.save_cookies(cookies)
            return True
            #if not defora: menu_principal(1)
      
      elif re.search('Erro',logintest) or link=='Erro':
            opcao= xbmcgui.Dialog().yesno('Lolabits.es', traducao(40005), "", "",traducao(40006), 'OK')
            return False
            #if opcao: menu_principal(0)
            #else: login_lolabits()
      else: return False
            

################################################### MENUS PLUGIN ######################################################

def menu_principal(ligacao):
      if ligacao==1:
            # addDir('[B][COLOR red]Addon em actualização/manutenção! Possíveis bugs.[/COLOR][/B]',MainURL,1,wtpath + art + 'pasta.png',1,False)
            # addDir(traducao(40007),MainURL,1,wtpath + art + 'pasta.png',1,True)            
            if status_lolabits: addDir('Mi Lolabits',MainURL + username_lb,3,wtpath + art + 'pasta.png',2,True)            
            if status_lolabits: addDir('Ir a Lolabits de otro usuario','pastas',5,wtpath + art + 'pasta.png',2,True)
            
            addDir(traducao(40037),MainURL,9,wtpath + art + 'pasta.png',2,True)
            #addDir('Atalhos',MainURL,18,wtpath + art + 'pasta.png',2,True)
            addDir(traducao(40011),'pesquisa',7,wtpath + art + 'pasta.png',3,True)
      elif ligacao==0:
            addDir(traducao(40015),MainURL,6,wtpath + art + 'pasta.png',1,True)
      #if ligacao==1: #addLink("[COLOR blue][B]%s:[/B][/COLOR] %s  [COLOR blue][B]%s:[/B][/COLOR] %s" % (traducao(40012),mensagens,traducao(40014),pontos),'',wtpath + art + 'pasta.png')
      #addDir("[COLOR blue][B]%s[/B][/COLOR] | abelhas.pt" % (traducao(40018)),MainURL,8,wtpath + art + 'pasta.png',6,True)
      xbmc.executebuiltin("Container.SetViewMode(51)")

def entrarnovamente(opcoes):
      if opcoes==1: selfAddon.openSettings()
      addDir(traducao(40020),MainURL,None,wtpath + art + 'refresh.png',1,True)
      addDir(traducao(40021),MainURL,8,wtpath + art + 'defs.png',1,False)

def topcolecionadores():
      if status_lolabits:
            conteudo=clean(abrir_url_cookie('http://lolabits.es/' + username_lb))
            users=re.compile('<li><div class="friend avatar"><a href="/(.+?)" title="(.+?)"><img alt=".+?" src="(.+?)" /><span></span></a></div>.+?<i>(.+?)</i></li>').findall(conteudo)
            for urluser,nomeuser,thumbuser,nruser in users:
                  addDir('[B][COLOR gold]' + nruser + 'º Abelhas[/B][/COLOR] ' + nomeuser,MainURL + urluser,3,thumbuser,len(users),True)      
      #xbmc.executebuiltin("Container.SetViewMode(500)")
      xbmcplugin.setContent(int(sys.argv[1]), 'livetv')

def abelhasmaisrecentes(url):
      if status_lolabits:
            conteudo=clean(abrir_url_cookie('http://lolabits.es/action/LastAccounts/MoreAccounts'))
            users=re.compile('<div class="friend avatar"><a href="/(.+?)" title="(.+?)"><img alt=".+?" src="(.+?)" /><span>').findall(conteudo)
            for urluser,nomeuser,thumbuser in users:
                  addDir('[B][COLOR gold]' + nomeuser + '[/B][/COLOR]',MainURL + urluser,3,thumbuser,len(users),True)      
      #xbmc.executebuiltin("Container.SetViewMode(500)")
      xbmcplugin.setContent(int(sys.argv[1]), 'livetv')

def pesquisa():
      if status_lolabits: conteudo=clean(abrir_url_cookie('http://lolabits.es/action/Help'))      
      opcoeslabel=re.compile('<option value=".+?">(.+?)</option>').findall(conteudo)
      opcoesvalue=re.compile('<option value="(.+?)">.+?</option>').findall(conteudo)
      index = xbmcgui.Dialog().select(traducao(40022), opcoeslabel)
      if index > -1:
            caixadetexto('pesquisa',ftype=opcoesvalue[index])
      else:sys.exit(0)

def favoritos():
      if status_lolabits:
         conteudo=abrir_url_cookie(MainURL + username_lb)
         chomikid=re.compile('<input id="FriendsTargetChomikName" name="FriendsTargetChomikName" type="hidden" value="(.+?)" />').findall(conteudo)[0]
         token=re.compile('<input name="__RequestVerificationToken" type="hidden" value="(.+?)" />').findall(conteudo)[0]

         if name==traducao(40037):pagina=1
         else: pagina=int(name.replace("[COLOR gold]Página ",'').replace(' >>>[/COLOR]',''))
         form_d = {'page':pagina,'chomikName':chomikid,'__RequestVerificationToken':token}
         ref_data = {'Accept':'*/*','Content-Type':'application/x-www-form-urlencoded','Host':'lolabits.es','Origin':'http://lolabits.es','Referer':url,'User-Agent':user_agent,'X-Requested-With':'XMLHttpRequest'}
         endlogin=MainURL + 'action/Friends/ShowAllFriends'
         info= net.http_POST(endlogin,form_data=form_d,headers=ref_data).content.encode('latin-1','ignore')
         info=info.replace('javascript:;','/javascript:;')
         users=re.compile('<div class="friend avatar".+?<a href="/(.+?)" title="(.+?)"><img alt=".+?" src="(.+?)" />').findall(info)
         for urluser,nomeuser,thumbuser in users:
            addDir(nomeuser,MainURL + urluser,3,thumbuser,len(users),True)
         paginas(info)      
      xbmc.executebuiltin("Container.SetViewMode(500)")
      xbmcplugin.setContent(int(sys.argv[1]), 'livetv')


def proxpesquisa_ab():
    from t0mm0.common.addon import Addon
    addon=Addon(addon_id)
    form_d=addon.load_data('temp.txt')
    ref_data = {'Accept':'*/*','Content-Type':'application/x-www-form-urlencoded','Host':'lolabits.es','Origin':'http://lolabits.es','Referer':url,'User-Agent':user_agent,'X-Requested-With':'XMLHttpRequest'}
    form_d['Page']= form_d['Page'] + 1
    endlogin=MainURL + 'action/SearchFiles/Results'
    net.set_cookies(cookies)
    conteudo= net.http_POST(endlogin,form_data=form_d,headers=ref_data).content.encode('latin-1','ignore')
    addon.save_data('temp.txt',form_d)
    pastas(MainURL + 'action/nada','coco',conteudo=conteudo)

def atalhos(type=False):
      pastatracks = os.path.join(pastaperfil, "atalhos")
      if not os.path.exists(pastatracks):
            os.makedirs(pastatracks)
            savefile('ref.tmp','0',pastafinal=pastatracks)
      if type=='addfolder':
            ref=int(openfile('ref.tmp',pastafinal=pastatracks)) + 1
            builder='{"name":"""%s""","url":"""%s""","type":"folder"}' % (name,url)
            savefile('%s.txt' % ref,builder,pastafinal=pastatracks)
            savefile('ref.tmp',str(ref),pastafinal=pastatracks)
            xbmc.executebuiltin("XBMC.Notification(abelhas.pt,Atalho adicionado,'500000',"+iconpequeno.encode('utf-8')+")")
      elif type=='addfile':
            ref=int(openfile('ref.tmp',pastafinal=pastatracks)) + 1
            builder='{"name":"""%s""","url":"""%s""","type":"file"}' % (name,url)
            savefile('%s.txt' % ref,builder,pastafinal=pastatracks)
            savefile('ref.tmp',str(ref),pastafinal=pastatracks)
            xbmc.executebuiltin("XBMC.Notification(abelhas.pt,Atalho adicionado,'500000',"+iconpequeno.encode('utf-8')+")")
      elif type=='remove':
            try:os.remove(os.path.join(pastatracks,name))
            except:pass
            xbmc.executebuiltin("Container.Refresh")
            
      else:
            try:lista = os.listdir(pastatracks)
            except: lista=[]
            
            for atal in lista:
                  
                  content=openfile(atal,pastafinal=pastatracks)
                  
                  try:ftype=re.compile('"type":"(.+?)"').findall(content)[0]
                  except:ftype=''
                  try:fname=re.compile('"name":"""(.+?)"""').findall(content)[0]
                  except:fname=''
                  try:furl=re.compile('"url":"""(.+?)"""').findall(content)[0]
                  except:furl=''
                  path=urllib.unquote_plus('/'.join(''.join(furl.split(MainURL)).split('/')[:-1]).replace('*','%'))
                  if ftype=='file': addCont('%s (%s)' % (fname,path),furl,4,'',wtpath + art + 'file.png',len(lista),False,atalhos=atal)
                  elif ftype=='folder': addDir('%s (%s)' % (fname,path),furl,3,wtpath + art + 'pasta.png',len(lista),True,atalhos=atal)
                  xbmc.executebuiltin("Container.SetViewMode(51)")
                        
                  
            

def pastas(url,name,formcont={},conteudo='',past=False):      
      sitebase=MainURL
      host='lolabits.es'
      color='gold'

      if re.search('action/SearchFiles',url):
            ref_data = {'Host': host, 'Connection': 'keep-alive', 'Referer': 'http://'+host+'/','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','User-Agent':user_agent,'Referer': 'http://'+host+'/'}
            endlogin=sitebase + 'action/SearchFiles'
            conteudo= net.http_POST(endlogin,form_data=formcont,headers=ref_data).content.encode('latin-1','ignore')
            if re.search('El fichero n&#227;o fue encontrado',conteudo):
                  mensagemok(host,'Sin resultados.')
            try:
                  filename=re.compile('<input name="FileName" type="hidden" value="(.+?)" />').findall(conteudo)[0]
                  try:ftype=re.compile('<input name="FileType" type="hidden" value="(.+?)" />').findall(conteudo)[0]
                  except: ftype='All'

                  pagina=1
                  token=re.compile('<input name="__RequestVerificationToken" type="hidden" value="(.+?)"').findall(conteudo)[0]

                  form_d = {'IsGallery':'True','FileName':filename,'FileType':ftype,'ShowAdultContent':'True','Page':pagina,'__RequestVerificationToken':token}
                  from t0mm0.common.addon import Addon
                  addon=Addon(addon_id)
                  addon.save_data('temp.txt',form_d)
                  ref_data = {'Accept':'*/*','Content-Type':'application/x-www-form-urlencoded','Host':host,'Origin':'http://'+host,'Referer':url,'User-Agent':user_agent,'X-Requested-With':'XMLHttpRequest'}
                  endlogin=sitebase + 'action/SearchFiles/Results'
                  conteudo= net.http_POST(endlogin,form_data=form_d,headers=ref_data).content.encode('latin-1','ignore')
            except: pass
            
      else:
            if conteudo=='':
                  extra='?requestedFolderMode=filesList&fileListSortType=Name&fileListAscending=True'
                  conteudo=clean(abrir_url_cookie(url + extra))

      if re.search('ProtectedFolderChomikLogin',conteudo):
            chomikid=re.compile('<input id="ChomikId" name="ChomikId" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            folderid=re.compile('<input id="FolderId" name="FolderId" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            foldername=re.compile('<input id="FolderName" name="FolderName" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            token=re.compile('<input name="__RequestVerificationToken" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            passwordfolder=caixadetexto('password')
            

            form_d = {'ChomikId':chomikid,'FolderId':folderid,'FolderName':foldername,'Password':passwordfolder,'Remember':'true','__RequestVerificationToken':token}
            ref_data = {'Accept':'*/*','Content-Type':'application/x-www-form-urlencoded','Host':host,'Origin':'http://' + host,'Referer':url,'User-Agent':user_agent,'X-Requested-With':'XMLHttpRequest'}
            endlogin=sitebase + 'action/Files/LoginToFolder'
            teste= net.http_POST(endlogin,form_data=form_d,headers=ref_data).content.encode('latin-1','ignore')
            teste=urllib.unquote(teste)
            if re.search('IsSuccess":false',teste):
                  mensagemok('Erro',traducao(40002))
                  sys.exit(0)
            else:
                  pastas_ref(url)
      elif re.search('/action/UserAccess/LoginToProtectedWindow',conteudo):
            chomiktype=re.compile('<input id="ChomikType" name="ChomikType" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            sex=re.compile('<input id="Sex" name="Sex" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            accname=re.compile('<input id="AccountName" name="AccountName" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            isadult=re.compile('<input id="AdultFilter" name="AdultFilter" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            adultfilter=re.compile('<input id="AdultFilter" name="AdultFilter" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            
            passwordfolder=caixadetexto('password')
            form_d = {'Password':passwordfolder,'OK':'OK','RemeberMe':'true','IsAdult':isadult,'Sex':sex,'AccountName':accname,'AdultFilter':adultfilter,'ChomikType':chomiktype,'TargetChomikId':chomikid}
            ref_data = {'Accept':'*/*','Content-Type':'application/x-www-form-urlencoded','Host':host,'Origin':'http://'+host,'Referer':url,'User-Agent':user_agent,'X-Requested-With':'XMLHttpRequest'}
            endlogin=sitebase + 'action/UserAccess/LoginToProtectedWindow'
            teste= net.http_POST(endlogin,form_data=form_d,headers=ref_data).content.encode('latin-1','ignore')
            teste=urllib.unquote(teste)
            if re.search('<span class="field-validation-error">A password introduzida est',teste):
                  mensagemok('Lolabits.es',traducao(40002))
            else:
                  pastas_ref(url)
      else:
            try:
                  conta=re.compile('<div class="bigFileInfoRight">.+?<h3>(.+?)<span>(.+?)</span></h3>').findall(conteudo)[0]
                  nomeconta=re.compile('<input id="FriendsTargetChomikName" name="FriendsTargetChomikName" type="hidden" value="(.+?)" />').findall(conteudo)[0]
                  addLink('[COLOR blue][B]' + traducao(40023) + nomeconta + '[/B][/COLOR]: ' + conta[0] + conta[1],'',wtpath + art + 'star2.png')
            except: pass

            try:
                  checker=url.split('/')[:-1]
                  if len(checker) > 3 and not re.search('action/SearchFiles',url) and not re.search('/action/nada',url):
                        urlbefore='/'.join(checker)
                        addDir('[COLOR blue][B]Carpeta superior[/B][/COLOR]',urlbefore,3,wtpath + art + 'seta.png',1,True)
            except: pass

            try:
                  pastas=re.compile('<div id="foldersList">(.+?)</table>.+?').findall(conteudo)
                  seleccionados=re.compile('<a href="/(.+?)".+?title="(.+?)">(.+?)</a>').findall(pastas[0])
                  for urlpasta,nomepasta,password in seleccionados:
                        
                        if re.search('<span class="pass">',password): displock=' (' + traducao(40024)+')'
                        else:displock=''
                        addDir('[B][COLOR white]' + nomepasta + '[/COLOR][/B]' + displock,sitebase + urlpasta,3,wtpath + art + 'pasta.png',len(seleccionados),True)
            except: pass
            #contributo mafarricos com alteracoes, ty
            items1=re.compile('<a class="expanderHeader downloadAction" href="(.+?)" title="(.+?)">.+?</span>(.+?)</a>.+?<li><span>(.+?)</span></li>.+?<span class="downloadsCounter">.+?<li>(.+?)</li>').findall(conteudo)
            for urlficheiro,tituloficheiro,extensao,tamanhoficheiro,dataficheiro in items1:
                  extensao=extensao.replace(' ','')
                  tamanhoficheiro=tamanhoficheiro.replace(' ','')
                  if extensao=='.rar' or extensao=='.RAR' or extensao == '.zip' or extensao=='.ZIP' or extensao=='.7z' or extensao=='.7Z': thumb=wtpath + art + 'rar.png'
                  elif extensao=='.mp3' or extensao=='.MP3' or extensao=='.ogg' or extensao=='.OGG' or extensao=='.aac' or extensao=='.AAC' or extensao=='.m4a' or extensao=='.M4A' or extensao == '.wma' or extensao=='.WMA' or extensao=='.ac3' or extensao=='.AC3' or extensao=='.flac' or extensao=='.FLAC' or extensao=='.m3u' or extensao=='.M3U': thumb=wtpath + art + 'musica.png'
                  elif extensao=='.jpg' or extensao == '.JPG' or extensao == '.bmp' or extensao == '.BMP' or extensao=='.gif' or extensao=='.GIF' or extensao=='.png' or extensao=='.PNG': thumb=wtpath + art + 'foto.png'
                  elif extensao=='.mkv' or extensao == '.MKV' or extensao == '.ogm' or extensao == '.OGM' or extensao == '.avi' or extensao == '.AVI' or extensao=='.mp4' or extensao=='.MP4' or extensao=='.3gp' or extensao=='.3GP' or extensao=='.wmv' or extensao=='.WMV' or extensao=='.mpg' or extensao=='.MPG': thumb=wtpath + art + 'video.png'
                  else:thumb=wtpath + art + 'file.png'
                  tamanhoparavariavel=' (' + tamanhoficheiro + ')'
                  if past==False: modo=4
                  else: modo=22
                  addCont('[B][COLOR '+color+']' + tituloficheiro + extensao + '[/COLOR][/B]' + '[COLOR white]' + tamanhoparavariavel + '[/COLOR]',sitebase + urlficheiro,modo,tamanhoparavariavel,thumb,len(items1),past,False)
            #contributo mafarricos com alteracoes, ty
            items2=re.compile('<a class="downloadAction" href="(.+?)">\s+<span class="bold">(.+?)</span>(.+?)</a>.+?<li>(.+?)</li>.+?<li><span class="date">(.+?)</span></li>').findall(conteudo)
            for urlficheiro,tituloficheiro,extensao,tamanhoficheiro,dataficheiro in items2:
                  extensao=extensao.replace(' ','')
                  if extensao=='.rar' or extensao=='.RAR' or extensao == '.zip' or extensao=='.ZIP' or extensao=='.7z' or extensao=='.7Z': thumb=wtpath + art + 'rar.png'
                  elif extensao=='.mp3' or extensao=='.MP3' or extensao=='.ogg' or extensao=='.OGG' or extensao=='.aac' or extensao=='.AAC' or extensao=='.m4a' or extensao=='.M4A' or extensao == '.wma' or extensao=='.WMA' or extensao=='.ac3' or extensao=='.AC3' or extensao=='.flac' or extensao=='.FLAC' or extensao=='.m3u' or extensao=='.M3U': thumb=wtpath + art + 'musica.png'
                  elif extensao=='.jpg' or extensao == '.JPG' or extensao == '.bmp' or extensao == '.BMP' or extensao=='.gif' or extensao=='.GIF' or extensao=='.png' or extensao=='.PNG': thumb=wtpath + art + 'foto.png'
                  elif extensao=='.mkv' or extensao == '.MKV' or extensao == '.ogm' or extensao == '.OGM' or extensao == '.avi' or extensao == '.AVI' or extensao=='.mp4' or extensao=='.MP4' or extensao=='.3gp' or extensao=='.3GP' or extensao=='.wmv' or extensao=='.WMV' or extensao=='.mpg' or extensao=='.MPG': thumb=wtpath + art + 'video.png'
                  else:thumb=wtpath + art + 'file.png'
                  tamanhoparavariavel=' (' + tamanhoficheiro + ')'
                  if past==False: modo=4
                  else: modo=22
                  addCont('[B][COLOR '+color+']' + tituloficheiro + extensao + '[/COLOR][/B]' + '[COLOR white]' + tamanhoparavariavel + '[/COLOR]',sitebase + urlficheiro,modo,tamanhoparavariavel,thumb,len(items2),past,False)
            if not items1:
                  if not items2:
                        conteudo=clean(conteudo)
                        #isto ta feio
                        items3=re.compile('<li class="fileItemContainer">.+?<span class="bold">.+?</span>(.+?)</a>.+?<div class="thumbnail">.+?<a href="(.+?)".+?title="(.+?)">\s+<img.+?<div class="smallTab">.+?<li>(.+?)</li>.+?<span class="date">(.+?)</span>').findall(conteudo)
                        for extensao,urlficheiro,tituloficheiro,tamanhoficheiro,dataficheiro in items3:
                              tamanhoficheiro=tamanhoficheiro.replace(' ','')
                              extensao=extensao.replace(' ','')
                              tituloficheiro=tituloficheiro.replace(str(extensao),'')
                              thumb=wtpath + art + 'file.png'
                              tamanhoparavariavel=' (' + tamanhoficheiro + ')'
                              if past==False: modo=4
                              else: modo=22
                              addCont('[B][COLOR '+color+']' + tituloficheiro + extensao + '[/COLOR][/B]' + '[COLOR white]' + tamanhoparavariavel + '[/COLOR]',sitebase + urlficheiro,modo,tamanhoparavariavel,thumb,len(items2),past,False)
                              
            paginas(conteudo)
            
      xbmc.executebuiltin("Container.SetViewMode(51)")

def pastas_de_fora(url,name,formcont={},conteudo='',past=False):
	login_abelhas(True)
	source = xbmcgui.Dialog().select
	selectlist = []
	urllist = []
	formcont = {'submitSearchFiles': 'Procurar', 'FileType': 'video', 'IsGallery': 'False', 'FileName': name }
	if re.search('action/SearchFiles',url):
		ref_data = {'Host': 'lolabits.es', 'Connection': 'keep-alive', 'Referer': 'http://lolabits.es/','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','User-Agent':user_agent,'Referer': 'http://lolabits.es/'}
		endlogin=MainURL + 'action/SearchFiles'
		conteudo= net.http_POST(endlogin,form_data=formcont,headers=ref_data).content.encode('latin-1','ignore')
		if re.search('El fichero no fue encontrado',conteudo):
			mensagemok('Lolabits.es','Sin resultados.')
			sys.exit(0)
		try:
			filename=re.compile('<input name="FileName" type="hidden" value="(.+?)" />').findall(conteudo)[0]
			try:ftype=re.compile('<input name="FileType" type="hidden" value="(.+?)" />').findall(conteudo)[0]
			except: ftype='All'
			pagina=1
			token=re.compile('<input name="__RequestVerificationToken" type="hidden" value="(.+?)"').findall(conteudo)[0]
			form_d = {'IsGallery':'True','FileName':filename,'FileType':ftype,'ShowAdultContent':'True','Page':pagina,'__RequestVerificationToken':token}
			from t0mm0.common.addon import Addon
			addon=Addon(addon_id)
			addon.save_data('temp.txt',form_d)
			ref_data = {'Accept':'*/*','Content-Type':'application/x-www-form-urlencoded','Host':'lolabits.es','Origin':'http://lolabits.es','Referer':url,'User-Agent':user_agent,'X-Requested-With':'XMLHttpRequest'}
			endlogin=MainURL + 'action/SearchFiles/Results'
			conteudo= net.http_POST(endlogin,form_data=form_d,headers=ref_data).content.encode('latin-1','ignore')
		except: pass
	else:
		if conteudo=='':
			extra='?requestedFolderMode=filesList&fileListSortType=Name&fileListAscending=True'
			conteudo=clean(abrir_url_cookie(url + extra))
	if re.search('ProtectedFolderChomikLogin',conteudo):
		chomikid=re.compile('<input id="ChomikId" name="ChomikId" type="hidden" value="(.+?)" />').findall(conteudo)[0]
		folderid=re.compile('<input id="FolderId" name="FolderId" type="hidden" value="(.+?)" />').findall(conteudo)[0]
		foldername=re.compile('<input id="FolderName" name="FolderName" type="hidden" value="(.+?)" />').findall(conteudo)[0]
		token=re.compile('<input name="__RequestVerificationToken" type="hidden" value="(.+?)" />').findall(conteudo)[0]
		passwordfolder=caixadetexto('password')
		form_d = {'ChomikId':chomikid,'FolderId':folderid,'FolderName':foldername,'Password':passwordfolder,'Remember':'true','__RequestVerificationToken':token}
		ref_data = {'Accept':'*/*','Content-Type':'application/x-www-form-urlencoded','Host':'lolabits.es','Origin':'http://lolabits.es','Referer':url,'User-Agent':user_agent,'X-Requested-With':'XMLHttpRequest'}
		endlogin=MainURL + 'action/Files/LoginToFolder'
		teste= net.http_POST(endlogin,form_data=form_d,headers=ref_data).content.encode('latin-1','ignore')
		teste=urllib.unquote(teste)
		if re.search('IsSuccess":false',teste):
			mensagemok('Lolabits.es',traducao(40002))
			sys.exit(0)
		else:
			pastas_ref(url)
	elif re.search('/action/UserAccess/LoginToProtectedWindow',conteudo):
		chomikid=re.compile('<input id="TargetChomikId" name="TargetChomikId" type="hidden" value="(.+?)" />').findall(conteudo)[0]
		chomiktype=re.compile('<input id="ChomikType" name="ChomikType" type="hidden" value="(.+?)" />').findall(conteudo)[0]
		sex=re.compile('<input id="Sex" name="Sex" type="hidden" value="(.+?)" />').findall(conteudo)[0]
		accname=re.compile('<input id="AccountName" name="AccountName" type="hidden" value="(.+?)" />').findall(conteudo)[0]
		isadult=re.compile('<input id="AdultFilter" name="AdultFilter" type="hidden" value="(.+?)" />').findall(conteudo)[0]
		adultfilter=re.compile('<input id="AdultFilter" name="AdultFilter" type="hidden" value="(.+?)" />').findall(conteudo)[0]
		passwordfolder=caixadetexto('password')
		form_d = {'Password':passwordfolder,'OK':'OK','RemeberMe':'true','IsAdult':isadult,'Sex':sex,'AccountName':accname,'AdultFilter':adultfilter,'ChomikType':chomiktype,'TargetChomikId':chomikid}
		ref_data = {'Accept':'*/*','Content-Type':'application/x-www-form-urlencoded','Host':'lolabits.es','Origin':'http://lolabits.es','Referer':url,'User-Agent':user_agent,'X-Requested-With':'XMLHttpRequest'}
		endlogin=MainURL + 'action/UserAccess/LoginToProtectedWindow'
		teste= net.http_POST(endlogin,form_data=form_d,headers=ref_data).content.encode('latin-1','ignore')
		teste=urllib.unquote(teste)
		if re.search('<span class="field-validation-error">A password introduzida est',teste):
			mensagemok('Lolabits.es',traducao(40002))
			sys.exit(0)
		else:
			pastas_ref(url)
	else:
		try:
			conta=re.compile('<div class="bigFileInfoRight">.+?<h3>(.+?)<span>(.+?)</span></h3>').findall(conteudo)[0]
			nomeconta=re.compile('<input id="FriendsTargetChomikName" name="FriendsTargetChomikName" type="hidden" value="(.+?)" />').findall(conteudo)[0]
			addLink('[COLOR blue][B]' + traducao(40023) + nomeconta + '[/B][/COLOR]: ' + conta[0] + conta[1],'',wtpath + art + 'star2.png')
		except: pass
		try:
			checker=url.split('/')[:-1]
			if len(checker) > 3 and not re.search('action/SearchFiles',url) and not re.search('lolabits.es/action/nada',url):
				urlbefore='/'.join(checker)
				addDir('[COLOR blue][B]Carpeta superior[/B][/COLOR]',urlbefore,3,wtpath + art + 'seta.png',1,True)
		except: pass
		try:
			pastas=re.compile('<div id="foldersList">(.+?)</table>').findall(conteudo)[0]
			seleccionados=re.compile('<a href="/(.+?)".+?title="(.+?)">(.+?)</a>').findall(pastas)
			for urlpasta,nomepasta,password in seleccionados:
				if re.search('<span class="pass">',password): displock=' (' + traducao(40024)+')'
				else:displock=''
				addDir(nomepasta + displock,MainURL + urlpasta,3,wtpath + art + 'pasta.png',len(seleccionados),True)
		except: pass
		#contributo mafarricos com alteracoes, ty
		items1=re.compile('<li class="fileItemContainer">\s+<p class="filename">\s+<a class="downloadAction" href=".+?">    <span class="bold">.+?</span>(.+?)</a>\s+</p>\s+<div class="thumbnail">\s+<div class="thumbnailWrapper expType" rel="Image" style=".+?">\s+<a href="(.+?)" class="thumbImg" rel="highslide" style=".+?" title="(.+?)">\s+<img src=".+?" rel=".+?" alt=".+?" style=".+?"/>\s+</a>\s+</div>\s+</div>\s+<div class="smallTab">\s+<ul>\s+<li>\s+(.+?)</li>\s+<li><span class="date">(.+?)</span></li>').findall(conteudo)         
		for urlficheiro,tituloficheiro,extensao,tamanhoficheiro,dataficheiro in items1:
			extensao=extensao.replace(' ','')
			tamanhoficheiro=tamanhoficheiro.replace(' ','')
			if extensao=='.rar' or extensao=='.RAR' or extensao == '.zip' or extensao=='.ZIP' or extensao=='.7z' or extensao=='.7Z': thumb=wtpath + art + 'rar.png'
			elif extensao=='.mp3' or extensao=='.MP3' or extensao=='.ogg' or extensao=='.OGG' or extensao=='.aac' or extensao=='.AAC' or extensao=='.m4a' or extensao=='.M4A' or extensao == '.wma' or extensao=='.WMA' or extensao=='.ac3' or extensao=='.AC3' or extensao=='.flac' or extensao=='.FLAC' or extensao=='.m3u' or extensao=='.M3U': thumb=wtpath + art + 'musica.png'
			elif extensao=='.jpg' or extensao == '.JPG' or extensao == '.bmp' or extensao == '.BMP' or extensao=='.gif' or extensao=='.GIF' or extensao=='.png' or extensao=='.PNG': thumb=wtpath + art + 'foto.png'
			elif extensao=='.mkv' or extensao == '.MKV' or extensao == '.ogm' or extensao == '.OGM' or extensao == '.avi' or extensao == '.AVI' or extensao=='.mp4' or extensao=='.MP4' or extensao=='.3gp' or extensao=='.3GP' or extensao=='.wmv' or extensao=='.WMV' or extensao=='.mpg' or extensao=='.MPG': thumb=wtpath + art + 'video.png'
			else:thumb=wtpath + art + 'file.png'
			tamanhoparavariavel=' (' + tamanhoficheiro + ')'
			if past==False: modo=4
			else: modo=22
			addCont('[B]' + tituloficheiro + '[/B]' + tamanhoparavariavel,MainURL + urlficheiro,modo,tamanhoparavariavel,thumb,len(items1),past,False)                  
		#contributo mafarricos com alteracoes, ty
		items2=re.compile('<a class="downloadAction" href="(.+?)">\s+<span class="bold">(.+?)</span>(.+?)</a>.+?<li>(.+?)</li>.+?<li><span class="date">(.+?)</span></li>').findall(conteudo)
		for urlficheiro,tituloficheiro,extensao,tamanhoficheiro,dataficheiro in items2:
			extensao=extensao.replace(' ','')
			if extensao=='.rar' or extensao=='.RAR' or extensao == '.zip' or extensao=='.ZIP' or extensao=='.7z' or extensao=='.7Z': thumb=wtpath + art + 'rar.png'
			elif extensao=='.mp3' or extensao=='.MP3' or extensao=='.ogg' or extensao=='.OGG' or extensao=='.aac' or extensao=='.AAC' or extensao=='.m4a' or extensao=='.M4A' or extensao == '.wma' or extensao=='.WMA' or extensao=='.ac3' or extensao=='.AC3' or extensao=='.flac' or extensao=='.FLAC' or extensao=='.m3u' or extensao=='.M3U': thumb=wtpath + art + 'musica.png'
			elif extensao=='.jpg' or extensao == '.JPG' or extensao == '.bmp' or extensao == '.BMP' or extensao=='.gif' or extensao=='.GIF' or extensao=='.png' or extensao=='.PNG': thumb=wtpath + art + 'foto.png'
			elif extensao=='.mkv' or extensao == '.MKV' or extensao == '.ogm' or extensao == '.OGM' or extensao == '.avi' or extensao == '.AVI' or extensao=='.mp4' or extensao=='.MP4' or extensao=='.3gp' or extensao=='.3GP' or extensao=='.wmv' or extensao=='.WMV' or extensao=='.mpg' or extensao=='.MPG': thumb=wtpath + art + 'video.png'
			else:thumb=wtpath + art + 'file.png'
			tamanhoparavariavel=' (' + tamanhoficheiro + ')'
			if past==False: modo=4
			else: modo=22
			#addCont('[B]' + tituloficheiro + extensao + '[/B]' + tamanhoparavariavel,MainURL + urlficheiro,modo,tamanhoparavariavel,thumb,len(items2),past,False)
			if modo==4:
				selectlist.append('[B]' + tituloficheiro + extensao + '[/B]' + tamanhoparavariavel)
				urllist.append(MainURL + urlficheiro)
		if not items1:
			if not items2:
				conteudo=clean(conteudo)
				#isto ta feio
				items3=re.compile('<li class="fileItemContainer">.+?<span class="bold">.+?</span>(.+?)</a>.+?<div class="thumbnail">.+?<a href="(.+?)".+?title="(.+?)">\s+<img.+?<div class="smallTab">.+?<li>(.+?)</li>.+?<span class="date">(.+?)</span>').findall(conteudo)
				for extensao,urlficheiro,tituloficheiro,tamanhoficheiro,dataficheiro in items3:
					tamanhoficheiro=tamanhoficheiro.replace(' ','')
					thumb=wtpath + art + 'file.png'
					tamanhoparavariavel=' (' + tamanhoficheiro + ')'
					if past==False: modo=4
					else: modo=22
					#addCont('[B]' + tituloficheiro + '[/B]' + tamanhoparavariavel,MainURL + urlficheiro,modo,tamanhoparavariavel,thumb,len(items2),past,False) 
					if modo == 4:
						selectlist.append('[B]' + tituloficheiro + '[/B]' + tamanhoparavariavel)
						urllist.append(MainURL + urlficheiro)
						
		#paginas(conteudo)
	choose=source('Link a Abrir',selectlist)
	if choose > -1:	analyzer(urllist[choose])
	#xbmc.executebuiltin("Container.SetViewMode(51)")

def obterlistadeficheiros():
            string=[]
            nrdepaginas=71
            for i in xrange(1,int(nrdepaginas)+1):
                  url='http://abelhas.pt/qqcoisa,%s' % i
                  extra='?requestedFolderMode=filesList&fileListSortType=Name&fileListAscending=True'
                  conteudo=clean(abrir_url_cookie(url + extra))
                  items1=re.compile('<li class="fileItemContainer">\s+<p class="filename">\s+<a class="downloadAction" href=".+?">    <span class="bold">.+?</span>(.+?)</a>\s+</p>\s+<div class="thumbnail">\s+<div class="thumbnailWrapper expType" rel="Image" style=".+?">\s+<a href="(.+?)" class="thumbImg" rel="highslide" style=".+?" title="(.+?)">\s+<img src=".+?" rel=".+?" alt=".+?" style=".+?"/>\s+</a>\s+</div>\s+</div>\s+<div class="smallTab">\s+<ul>\s+<li>\s+(.+?)</li>\s+<li><span class="date">(.+?)</span></li>').findall(conteudo)         
                  for urlficheiro,tituloficheiro,extensao,tamanhoficheiro,dataficheiro in items1:
                        string.append(tituloficheiro)
                  #contributo mafarricos com alteracoes, ty
                  items2=re.compile('<a class="downloadAction" href="(.+?)">\s+<span class="bold">(.+?)</span>(.+?)</a>.+?<li>(.+?)</li>.+?<li><span class="date">(.+?)</span></li>').findall(conteudo)
                  for urlficheiro,tituloficheiro,extensao,tamanhoficheiro,dataficheiro in items2:
                        string.append(tituloficheiro)
                  if not items1:
                        if not items2:
                              conteudo=clean(conteudo)
                              #isto ta feio
                              items3=re.compile('<li class="fileItemContainer">.+?<span class="bold">.+?</span>(.+?)</a>.+?<div class="thumbnail">.+?<a href="(.+?)".+?title="(.+?)">\s+<img.+?<div class="smallTab">.+?<li>(.+?)</li>.+?<span class="date">(.+?)</span>').findall(conteudo)
                              for extensao,urlficheiro,tituloficheiro,tamanhoficheiro,dataficheiro in items3:
                                    string.append(tituloficheiro)
            print string


def criarplaylist(url,name,formcont={},conteudo=''):
   if re.search('minhateca.com.br',url):
      mensagemprogresso.create('Minhateca.com.br', traducao(40049))
      playlist = xbmc.PlayList(1)
      playlist.clear()
      if re.search('action/SearchFiles',url):
            ref_data = {'Host': 'minhateca.com.br', 'Connection': 'keep-alive', 'Referer': 'http://minhateca.com.br/','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','User-Agent':user_agent,'Referer': 'http://minhateca.com.br/'}
            endlogin=MinhaMainURL + 'action/SearchFiles'
            conteudo= net.http_POST(endlogin,form_data=formcont,headers=ref_data).content.encode('latin-1','ignore')
            if re.search('O ficheiro n.+?o foi encontrado',conteudo):
                  mensagemok('Minhateca.com.br','Sem resultados.')
                  sys.exit(0)
            try:
                  filename=re.compile('<input name="FileName" type="hidden" value="(.+?)">').findall(conteudo)[0]
                  try:ftype=re.compile('<input name="FileType" type="hidden" value="(.+?)">').findall(conteudo)[0]
                  except: ftype='All'
                  pagina=1
                  token=re.compile('<input name="__RequestVerificationToken" type="hidden" value="(.+?)"').findall(conteudo)[0]
                  form_d = {'IsGallery':'True','FileName':filename,'FileType':ftype,'ShowAdultContent':'True','Page':pagina,'__RequestVerificationToken':token}
                  from t0mm0.common.addon import Addon
                  addon=Addon(addon_id)
                  addon.save_data('temp.txt',form_d)
                  ref_data = {'Accept':'*/*','Content-Type':'application/x-www-form-urlencoded','Host':'minhateca.com.br','Origin':'http://minhateca.com.br','Referer':url,'User-Agent':user_agent,'X-Requested-With':'XMLHttpRequest'}
                  endlogin=MinhaMainURL + 'action/SearchFiles/Results'
                  conteudo= net.http_POST(endlogin,form_data=form_d,headers=ref_data).content.encode('latin-1','ignore')
            except: pass
      else:
            if conteudo=='':
                  extra='?requestedFolderMode=filesList&fileListSortType=Name&fileListAscending=True'
                  conteudo=clean(abrir_url_cookie(url + extra))
      if re.search('ProtectedFolderChomikLogin',conteudo):
            chomikid=re.compile('<input id="ChomikId" name="ChomikId" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            folderid=re.compile('<input id="FolderId" name="FolderId" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            foldername=re.compile('<input id="FolderName" name="FolderName" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            token=re.compile('<input name="__RequestVerificationToken" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            passwordfolder=caixadetexto('password')
            form_d = {'ChomikId':chomikid,'FolderId':folderid,'FolderName':foldername,'Password':passwordfolder,'Remember':'true','__RequestVerificationToken':token}
            ref_data = {'Accept':'*/*','Content-Type':'application/x-www-form-urlencoded','Host':'minhateca.com.br','Origin':'http://minhateca.com.br','Referer':url,'User-Agent':user_agent,'X-Requested-With':'XMLHttpRequest'}
            endlogin=MinhaMainURL + 'action/Files/LoginToFolder'
            teste= net.http_POST(endlogin,form_data=form_d,headers=ref_data).content.encode('latin-1','ignore')
            teste=urllib.unquote(teste)
            if re.search('IsSuccess":false',teste):
                  mensagemok('Minhateca.com.br',traducao(40002))
                  sys.exit(0)
            else: pastas_ref(url)
      elif re.search('/action/UserAccess/LoginToProtectedWindow',conteudo):
            chomikid=re.compile('<input id="TargetChomikId" name="TargetChomikId" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            chomiktype=re.compile('<input id="Mode" name="Mode" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            #sex=re.compile('<input id="Sex" name="Sex" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            accname=re.compile('<input id="__accno" name="__accno" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            #isadult=re.compile('<input id="AdultFilter" name="AdultFilter" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            #adultfilter=re.compile('<input id="AdultFilter" name="AdultFilter" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            passwordfolder=caixadetexto('password')
            form_d = {'Password':passwordfolder,'OK':'OK','RemeberMe':'true','AccountName':accname,'ChomikType':chomiktype,'TargetChomikId':chomikid}
            ref_data = {'Accept':'*/*','Content-Type':'application/x-www-form-urlencoded','Host':'minhateca.com.br','Origin':'http://minhateca.com.br','Referer':url,'User-Agent':user_agent,'X-Requested-With':'XMLHttpRequest'}
            endlogin=MinhaMainURL + 'action/UserAccess/LoginToProtectedWindow'
            teste= net.http_POST(endlogin,form_data=form_d,headers=ref_data).content.encode('latin-1','ignore')
            teste=urllib.unquote(teste)
            if re.search('<span class="field-validation-error">A password introduzida est',teste):
                  mensagemok('Minhateca.com.br',traducao(40002))
                  sys.exit(0)
            else: pastas_ref(url)
      else:
            items1=re.compile('<a class="expanderHeader downloadAction" href="(.+?)" title="(.+?)">.+?</span>(.+?)</a>.+?<li><span>(.+?)</span></li>.+?<span class="downloadsCounter">.+?<li>(.+?)</li>').findall(conteudo)
            for urlficheiro,tituloficheiro,extensao,tamanhoficheiro,dataficheiro in items1: analyzer(MinhaMainURL + urlficheiro,subtitles='',playterm='playlist',playlistTitle=tituloficheiro)
            items2=re.compile('<a class="downloadAction" href="(.+?)">\s+<span class="bold">(.+?)</span>(.+?)</a>.+?<li>(.+?)</li>.+?<li><span class="date">(.+?)</span></li>').findall(conteudo)
            for urlficheiro,tituloficheiro,extensao,tamanhoficheiro,dataficheiro in items2: analyzer(MinhaMainURL + urlficheiro,subtitles='',playterm='playlist',playlistTitle=tituloficheiro)
            if not items1:
                  if not items2:
                        conteudo=clean(conteudo)
                        #isto ta feio
                        items3=re.compile('<li class="fileItemContainer">.+?<span class="bold">.+?</span>(.+?)</a>.+?<div class="thumbnail">.+?<a href="(.+?)".+?title="(.+?)">\s+<img.+?<div class="smallTab">.+?<li>(.+?)</li>.+?<span class="date">(.+?)</span>').findall(conteudo)
                        for extensao,urlficheiro,tituloficheiro,tamanhoficheiro,dataficheiro in items3:
                              tamanhoficheiro=tamanhoficheiro.replace(' ','')
                              analyzer(MinhaMainURL + urlficheiro,subtitles='',playterm='playlist',playlistTitle=tituloficheiro)
   else:
      mensagemprogresso.create('Abelhas.pt', traducao(40049))
      playlist = xbmc.PlayList(1)
      playlist.clear()
      if re.search('action/SearchFiles',url):
            ref_data = {'Host': 'lolabits.es', 'Connection': 'keep-alive', 'Referer': 'http://lolabits.es/','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','User-Agent':user_agent,'Referer': 'http://abelhas.pt/'}
            endlogin=MainURL + 'action/SearchFiles'
            conteudo= net.http_POST(endlogin,form_data=formcont,headers=ref_data).content.encode('latin-1','ignore')
            if re.search('O ficheiro n.+?o foi encontrado',conteudo):
                  mensagemok('Lolabits.es','Sem resultados.')
                  sys.exit(0)
            try:
                  filename=re.compile('<input name="FileName" type="hidden" value="(.+?)" />').findall(conteudo)[0]
                  try:ftype=re.compile('<input name="FileType" type="hidden" value="(.+?)" />').findall(conteudo)[0]
                  except: ftype='All'
                  pagina=1
                  token=re.compile('<input name="__RequestVerificationToken" type="hidden" value="(.+?)"').findall(conteudo)[0]
                  form_d = {'IsGallery':'True','FileName':filename,'FileType':ftype,'ShowAdultContent':'True','Page':pagina,'__RequestVerificationToken':token}
                  from t0mm0.common.addon import Addon
                  addon=Addon(addon_id)
                  addon.save_data('temp.txt',form_d)
                  ref_data = {'Accept':'*/*','Content-Type':'application/x-www-form-urlencoded','Host':'lolabits.es','Origin':'http://lolabits.es','Referer':url,'User-Agent':user_agent,'X-Requested-With':'XMLHttpRequest'}
                  endlogin= MainURL+ 'action/SearchFiles/Results'
                  conteudo= net.http_POST(endlogin,form_data=form_d,headers=ref_data).content.encode('latin-1','ignore')
            except: pass
      else:
            if conteudo=='':
                  extra='?requestedFolderMode=filesList&fileListSortType=Name&fileListAscending=True'
                  conteudo=clean(abrir_url_cookie(url + extra))
      if re.search('ProtectedFolderChomikLogin',conteudo):
            chomikid=re.compile('<input id="ChomikId" name="ChomikId" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            folderid=re.compile('<input id="FolderId" name="FolderId" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            foldername=re.compile('<input id="FolderName" name="FolderName" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            token=re.compile('<input name="__RequestVerificationToken" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            passwordfolder=caixadetexto('password')
            form_d = {'ChomikId':chomikid,'FolderId':folderid,'FolderName':foldername,'Password':passwordfolder,'Remember':'true','__RequestVerificationToken':token}
            ref_data = {'Accept':'*/*','Content-Type':'application/x-www-form-urlencoded','Host':'lolabits.es','Origin':'http://lolabits.es','Referer':url,'User-Agent':user_agent,'X-Requested-With':'XMLHttpRequest'}
            endlogin=MainURL + 'action/Files/LoginToFolder'
            teste= net.http_POST(endlogin,form_data=form_d,headers=ref_data).content.encode('latin-1','ignore')
            teste=urllib.unquote(teste)
            if re.search('IsSuccess":false',teste):
                  mensagemok('Lolabits.es',traducao(40002))
                  sys.exit(0)
            else: pastas_ref(url)
      elif re.search('/action/UserAccess/LoginToProtectedWindow',conteudo):
            chomikid=re.compile('<input id="TargetChomikId" name="TargetChomikId" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            chomiktype=re.compile('<input id="Mode" name="Mode" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            #sex=re.compile('<input id="Sex" name="Sex" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            accname=re.compile('<input id="__accno" name="__accno" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            #isadult=re.compile('<input id="AdultFilter" name="AdultFilter" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            #adultfilter=re.compile('<input id="AdultFilter" name="AdultFilter" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            passwordfolder=caixadetexto('password')
            form_d = {'Password':passwordfolder,'OK':'OK','RemeberMe':'true','AccountName':accname,'ChomikType':chomiktype,'TargetChomikId':chomikid}
            ref_data = {'Accept':'*/*','Content-Type':'application/x-www-form-urlencoded','Host':'lolabits.es','Origin':'http://lolabits.es','Referer':url,'User-Agent':user_agent,'X-Requested-With':'XMLHttpRequest'}
            endlogin=MainURL + 'action/UserAccess/LoginToProtectedWindow'
            teste= net.http_POST(endlogin,form_data=form_d,headers=ref_data).content.encode('latin-1','ignore')
            teste=urllib.unquote(teste)
            if re.search('<span class="field-validation-error">A password introduzida est',teste):
                  mensagemok('Lolabits.es',traducao(40002))
                  sys.exit(0)
            else: pastas_ref(url)
      else:
            items1=re.compile('<a class="expanderHeader downloadAction" href="(.+?)" title="(.+?)">.+?</span>(.+?)</a>.+?<li><span>(.+?)</span></li>.+?<span class="downloadsCounter">.+?<li>(.+?)</li>').findall(conteudo)
            for urlficheiro,tituloficheiro,extensao,tamanhoficheiro,dataficheiro in items1: analyzer(MainURL + urlficheiro,subtitles='',playterm='playlist',playlistTitle=tituloficheiro)
            items2=re.compile('<a class="downloadAction" href="(.+?)">\s+<span class="bold">(.+?)</span>(.+?)</a>.+?<li>(.+?)</li>.+?<li><span class="date">(.+?)</span></li>').findall(conteudo)
            for urlficheiro,tituloficheiro,extensao,tamanhoficheiro,dataficheiro in items2: analyzer(MainURL + urlficheiro,subtitles='',playterm='playlist',playlistTitle=tituloficheiro)
            if not items1:
                  if not items2:
                        conteudo=clean(conteudo)
                        #isto ta feio
                        items3=re.compile('<li class="fileItemContainer">.+?<span class="bold">.+?</span>(.+?)</a>.+?<div class="thumbnail">.+?<a href="(.+?)".+?title="(.+?)">\s+<img.+?<div class="smallTab">.+?<li>(.+?)</li>.+?<span class="date">(.+?)</span>').findall(conteudo)
                        for extensao,urlficheiro,tituloficheiro,tamanhoficheiro,dataficheiro in items3:
                              tamanhoficheiro=tamanhoficheiro.replace(' ','')
                              analyzer(MainURL + urlficheiro,subtitles='',playterm='playlist',playlistTitle=tituloficheiro)
      mensagemprogresso.close()
      xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
      xbmcPlayer.play(playlist)

def pastas_ref(url):
      pastas(url,name)

def paginas(link):
      
      sitebase=MainURL
      nextname='Lolabits'
      color='gold'
      mode=12

      try:
            idmode=3
      
            try:
                  conteudo=re.compile('<div id="listView".+?>(.+?)<div class="filerow fileItemContainer">').findall(link)[0]
                  
            except:
                  try:conteudo=re.compile('<div class="paginator clear searchListPage">(.+?)<div class="clear">').findall(link)[0]
                  except:
                        conteudo=re.compile('<div class="paginator clear friendspager">(.+?)<div class="clear">').findall(link)[0]
                        idmode=9
            try:
                  pagina=re.compile('anterior.+?<a href="/(.+?)" class="right" rel="(.+?)"').findall(conteudo)[0]
                  urlpag=pagina[0]
                  urlpag=urlpag.replace(' ','+')
                  addDir('[COLOR '+color+']Página ' + pagina[1] + ' ' + nextname + ' >>>[/COLOR]',sitebase + urlpag,idmode,wtpath + art + 'seta.png',1,True)
            except:
                  nrpagina=re.compile('type="hidden" value="([^"]+?)" /><input type="submit" value="p.+?gina seguinte.+?" /></form>').findall(link)[0]
                  addDir('[COLOR '+color+']Página ' + nrpagina + ' ' + nextname + ' >>>[/COLOR]',sitebase,mode,wtpath + art + 'seta.png',1,True)
                  #pass
                  
      
            
      except:
            pass


########################################################### PLAYER ################################################

def analyzer(url,subtitles='',playterm=False,playlistTitle=''):      

      sitebase=MainURL
      host='lolabits.es'
      sitename='Lolabits.es'
      
      if playlistTitle == '': mensagemprogresso.create(sitename, traducao(40025))
      linkfinal=''
      if subtitles=='sim': conteudo=abrir_url_cookie(url)
      else:conteudo=abrir_url_cookie(url,erro=False)
      if re.search('Pode acontecer que a mensagem de confirma',conteudo):
            mensagemok(sitename,'Necessitas de activar a tua conta '+sitename+'.')
            return
      try:
            fileid=re.compile('<input type="hidden" name="FileId" value="(.+?)"/>').findall(conteudo)[0]
            token=re.compile('<input name="__RequestVerificationToken" type="hidden" value="(.+?)" />').findall(conteudo)[0]
            form_d = {'fileId':fileid,'__RequestVerificationToken':token}
            ref_data = {'Accept': '*/*', 'Content-Type': 'application/x-www-form-urlencoded','Origin': 'http://' + host, 'X-Requested-With': 'XMLHttpRequest', 'Referer': 'http://'+host+'/','User-Agent':user_agent}
            endlogin=sitebase + 'action/License/Download'
            final= net.http_POST(endlogin,form_data=form_d,headers=ref_data).content.encode('latin-1','ignore')
            final=final.replace('\u0026','&').replace('\u003c','<').replace('\u003e','>').replace('\\','')
      except: pass
      try:
            if re.search('action/License/acceptLargeTransfer',final):
                  fileid=re.compile('<input type="hidden" name="fileId" value="(.+?)"').findall(final)[0]
                  orgfile=re.compile('<input type="hidden" name="orgFile" value="(.+?)"').findall(final)[0]
                  userselection=re.compile('<input type="hidden" name="userSelection" value="(.+?)"').findall(final)[0]
                  form_d = {'fileId':fileid,'orgFile':orgfile,'userSelection':userselection,'__RequestVerificationToken':token}
                  ref_data = {'Accept': '*/*', 'Content-Type': 'application/x-www-form-urlencoded','Origin': 'http://' + sitebase, 'X-Requested-With': 'XMLHttpRequest', 'Referer': 'http://'+sitebase+'/','User-Agent':user_agent}
                  endlogin=sitebase + 'action/License/acceptLargeTransfer'
                  final= net.http_POST(endlogin,form_data=form_d,headers=ref_data).content.encode('latin-1','ignore')
      except: pass
      try:
            if re.search('causar problemas com o uso de aceleradores de download',final):linkfinal=re.compile('a href=\"(.+?)\"').findall(final)[0]
            else: linkfinal=re.compile('"redirectUrl":"(.+?)"').findall(final)[0]
            if subtitles=='sim':return linkfinal
      except:
            if subtitles=='':
                  if re.search('Por favor, intente bajar el fichero más tarde.',final):
                        mensagemok(sitename,traducao(40026))
                        return
                  else:
                        mensagemok(sitename,traducao(40027))
                        print str(final)
                        print str(linkfinal) 
                        return
            else: return

      if playlistTitle == '': mensagemprogresso.close()
      linkfinal=linkfinal.replace('\u0026','&').replace('\u003c','<').replace('\u003e','>').replace('\\','')
      if re.search('.jpg',url) or re.search('.png',url) or re.search('.gif',url) or re.search('.bmp',url):
            if re.search('.jpg',url): extfic='temp.jpg'
            elif re.search('.png',url): extfic='temp.png'
            elif re.search('.gif',url): extfic='temp.gif'
            elif re.search('.bmp',url): extfic='temp.bmp'
            fich=os.path.join(pastaperfil, extfic)
            try:os.remove(fich)
            except:pass
            if playterm=="download":fazerdownload(extfic,linkfinal)
            else:fazerdownload(extfic,linkfinal,tipo="fotos")
            xbmc.executebuiltin("SlideShow("+pastaperfil+")")
      elif re.search('.mkv',url) or re.search('.ogm',url) or re.search('.avi',url) or re.search('.wmv',url) or re.search('.mp4',url) or re.search('.mpg',url) or re.search('.mpeg',url):
            endereco=legendas(fileid,url)
            if playlistTitle <> '': comecarvideo(playlistTitle,linkfinal,playterm=playterm,legendas=endereco)
            else: comecarvideo(name,linkfinal,playterm=playterm,legendas=endereco)
      elif re.search('.mp3',url) or re.search('.aac',url) or re.search('.m4a',url) or re.search('.ac3',url) or re.search('.wma',url):
            if playlistTitle <> '': comecarvideo(playlistTitle,linkfinal,playterm=playterm)
            else: comecarvideo(name,linkfinal,playterm=playterm)
      else:
            if selfAddon.getSetting('aviso-extensao') == 'true': mensagemok(sitename,traducao(40028),traducao(40029),traducao(40030))
            if playlistTitle <> '': comecarvideo(playlistTitle,linkfinal,playterm=playterm)
            else: comecarvideo(name,linkfinal,playterm=playterm)

def legendas(moviefileid,url):
      url=url.replace(','+moviefileid,'').replace('.mkv','.srt').replace('.mp4','.srt').replace('.avi','.srt').replace('.wmv','.srt')[:-7]
      legendas=analyzer(url,subtitles='sim')
      return legendas

def comecarvideo(name,url,playterm,legendas=None):        
        sitename='Lolabits - '+name      
        playeractivo = xbmc.getCondVisibility('Player.HasMedia')
        if playterm=='download':
              fazerdownload(name,url)
              return
        thumbnail=''
        playlist = xbmc.PlayList(1)
        if not playterm and playeractivo==0: playlist.clear()
        listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=thumbnail)
        #listitem.setInfo("Video", {"Title":"Balas & Bolinhos","year":2001})
        title='%s' % (name.split('[/B]')[0].replace('[B]',''))

        listitem.setInfo("Video", {"Title":title})
        listitem.setInfo("Music", {"Title":title})
        listitem.setProperty('mimetype', 'video/x-msvideo')
        listitem.setProperty('IsPlayable', 'true')
        if playterm <> 'playlist':
              dialogWait = xbmcgui.DialogProgress()
              dialogWait.create('Video', 'Cargando')
        playlist.add(url, listitem)
        if playterm <> 'playlist':		
              dialogWait.close()
              del dialogWait
        xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
        if not playterm and playeractivo==0:
              
              xbmcPlayer.play(playlist)
        if legendas!=None: xbmcPlayer.setSubtitles(legendas)
        else:
			if selfAddon.getSetting("subtitles") == 'true': 
				try: totalTime = xbmc.Player().getTotalTime()
				except: totalTime = 0
				print '##totaltime',totalTime
				if totalTime >= int(selfAddon.getSetting("minsize"))*60:
					print '#pesquisar legendas'
					from resources.lib import subtitles
					legendas = subtitles.getsubtitles(name,selfAddon.getSetting("sublang1"),selfAddon.getSetting("sublang2"))
					if legendas!=None: xbmcPlayer.setSubtitles(legendas)
        if playterm=='playlist': xbmc.executebuiltin("XBMC.Notification("+sitename+","+traducao(40039)+",'500000',"+iconpequeno.encode('utf-8')+")")

def limparplaylist():
        playlist = xbmc.PlayList(1)
        playlist.clear()
        xbmc.executebuiltin("XBMC.Notification(abelhas.pt,"+traducao(40048)+",'500000',"+iconpequeno.encode('utf-8')+")")

def comecarplaylist():
        playlist = xbmc.PlayList(1)
        if playlist:
              xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
              xbmcPlayer.play(playlist)

################################################## PASTAS ################################################################

def addLink(name,url,iconimage):
      liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
      liz.setInfo( type="Video", infoLabels={ "Title": name } )
      liz.setProperty('fanart_image', "%s/fanart.jpg"%selfAddon.getAddonInfo("path"))
      return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)

def addDir(name,url,mode,iconimage,total,pasta,atalhos=False):
      contexto=[]
      u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
      liz=xbmcgui.ListItem(name,iconImage="DefaultFolder.png", thumbnailImage=iconimage)
      contexto.append((traducao(40050), 'XBMC.RunPlugin(%s?mode=15&url=%s&name=%s)' % (sys.argv[0], urllib.quote_plus(url),name)))
      contexto.append((traducao(40047), 'XBMC.RunPlugin(%s?mode=14&url=%s&name=%s)' % (sys.argv[0], urllib.quote_plus(url),name)))
      contexto.append(('Ver Trailer', 'RunPlugin(%s?mode=17&url=%s&name=%s)' % (sys.argv[0],urllib.quote_plus(url),name)))
      if atalhos==False:contexto.append(('Adicionar atalho', 'RunPlugin(%s?mode=20&url=%s&name=%s)' % (sys.argv[0],urllib.quote_plus(url),name)))
      else:contexto.append(('Remover atalho', 'RunPlugin(%s?mode=21&url=%s&name=%s)' % (sys.argv[0],urllib.quote_plus(url),atalhos)))
      liz.setInfo( type="Video", infoLabels={ "Title": name} )
      liz.setProperty('fanart_image', "%s/fanart.jpg"%selfAddon.getAddonInfo("path"))
      liz.addContextMenuItems(contexto, replaceItems=False) 
      return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)

def addCont(name,url,mode,tamanho,iconimage,total,pasta=False,atalhos=False):
      contexto=[]
      u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&tamanhof="+urllib.quote_plus(tamanho)
      liz=xbmcgui.ListItem(name,iconImage="DefaultFolder.png", thumbnailImage=iconimage)
      contexto.append((traducao(40038), 'XBMC.RunPlugin(%s?mode=10&url=%s&name=%s)' % (sys.argv[0], urllib.quote_plus(url),name)))
      contexto.append((traducao(40046), 'XBMC.RunPlugin(%s?mode=13&url=%s&name=%s)' % (sys.argv[0], urllib.quote_plus(url),name)))
      contexto.append((traducao(40047), 'XBMC.RunPlugin(%s?mode=14&url=%s&name=%s)' % (sys.argv[0], urllib.quote_plus(url),name)))
      contexto.append(('Ver Trailer', 'RunPlugin(%s?mode=17&url=%s&name=%s)' % (sys.argv[0],urllib.quote_plus(url),name)))
      if atalhos==False: contexto.append(('Adicionar atalho', 'RunPlugin(%s?mode=19&url=%s&name=%s)' % (sys.argv[0],urllib.quote_plus(url),name)))
      else: contexto.append(('Remover atalho', 'RunPlugin(%s?mode=21&url=%s&name=%s)' % (sys.argv[0],urllib.quote_plus(url),atalhos)))
      contexto.append((traducao(40040), 'XBMC.RunPlugin(%s?mode=11&url=%s&name=%s&tamanhof=%s)' % (sys.argv[0], urllib.quote_plus(url),name,tamanho)))
      liz.setInfo( type="Video", infoLabels={ "Title": name} )
      liz.setProperty('fanart_image', "%s/fanart.jpg"%selfAddon.getAddonInfo("path"))
      liz.addContextMenuItems(contexto, replaceItems=True) 
      return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)
           
######################################################## DOWNLOAD ###############################################
### THANKS ELDORADO (ICEFILMS) ###
def fazerdownload(name,url,tipo="outros"):
      vidname=name.replace('[B]','').replace('[/B]','').replace('\\','').replace(str(tamanhoparavariavel),'')
      vidname = re.sub('[^-a-zA-Z0-9_.()\\\/ ]+', '',  vidname)
      dialog = xbmcgui.Dialog()
      if tipo=="fotos":
            mypath=os.path.join(pastaperfil, vidname)
      else:
            downloadPath = dialog.browse(int(3), traducao(40041),'myprograms')
            if os.path.exists(downloadPath):
                  mypath=os.path.join(downloadPath,vidname)
            else: return

      if os.path.isfile(mypath) is True:
            ok = mensagemok('Abelhas.pt',traducao(40042),'','')
            return False
      else:              
            try:
                  dp = xbmcgui.DialogProgress()
                  dp.create('Abelhas.pt - ' + traducao(40043), '', name)
                  start_time = time.time()
                  try: urllib.urlretrieve(url, mypath, lambda nb, bs, fs: dialogdown(nb, bs, fs, dp, start_time))
                  except:
                        while os.path.exists(mypath): 
                              try: os.remove(mypath); break 
                              except: pass 
                        if sys.exc_info()[0] in (urllib.ContentTooShortError, StopDownloading, OSError): return False 
                        else: raise 
                        return False
                  return True
            except: ok=mensagemok('Lolabits.es',traducao(40044)); print 'download failed'; return False

def dialogdown(numblocks, blocksize, filesize, dp, start_time):
      try:
            percent = min(numblocks * blocksize * 100 / filesize, 100)
            currently_downloaded = float(numblocks) * blocksize / (1024 * 1024) 
            kbps_speed = numblocks * blocksize / (time.time() - start_time) 
            if kbps_speed > 0: eta = (filesize - numblocks * blocksize) / kbps_speed 
            else: eta = 0 
            kbps_speed = kbps_speed / 1024 
            total = float(filesize) / (1024 * 1024) 
            mbs = '%.02f MB de %.02f MB' % (currently_downloaded, total) 
            #e = 'Velocidade: (%.0f Kb/s) ' % kbps_speed
            e = ' (%.0f Kb/s) ' % kbps_speed 
            tempo = traducao(40045) + ': %02d:%02d' % divmod(eta, 60) 
            dp.update(percent, mbs + e,tempo)
            #if percent=xbmc.executebuiltin("XBMC.Notification(Abelhas.pt,"+ mbs + e + ",'500000',"+iconpequeno+")")
      except: 
            percent = 100 
            dp.update(percent) 
      if dp.iscanceled(): 
            dp.close()
            raise StopDownloading('Stopped Downloading')

class StopDownloading(Exception):
      def __init__(self, value): self.value = value 
      def __str__(self): return repr(self.value)

######################################################## OUTRAS FUNCOES ###############################################

def caixadetexto(url,ftype=''):
      ultpes=''
      save=False
      if url=='pastas' and re.search('Abelha',name): title="Ir a - Lolabits"
      elif url=='pastas' and re.search('Minhateca',name): title="Ir para - Minhateca"
      elif url=='password': title="Contraseña - Lolabits.es"
      elif url=='pesquisa':
            title=traducao(40031)
            ultpes=selfAddon.getSetting('ultima-pesquisa')
            save=True
      else: title="Lolabits.es"
      keyb = xbmc.Keyboard(ultpes, title)
      keyb.doModal()
      if (keyb.isConfirmed()):
            search = keyb.getText()
            if search=='': sys.exit(0)
            encode=urllib.quote_plus(search)
            if save==True: selfAddon.setSetting('ultima-pesquisa', search)
            if url=='pastas' and re.search('Abelha',name): pastas(MainURL + search,name)
            elif url=='pastas' and re.search('Minhateca',name): pastas(MinhaMainURL + search,name) 
            elif url=='password': return search
            elif url=='pesquisa':
                  if status_lolabits:
                        form_d = {'FileName':encode,'submitSearchFiles':'Procurar','FileType':ftype,'IsGallery':'False'}
                        pastas(MainURL + 'action/SearchFiles',name,formcont=form_d,past=True)                  
            
      else: sys.exit(0)
            
def abrir_url(url):
      req = urllib2.Request(url)
      req.add_header('User-Agent', user_agent)
      response = urllib2.urlopen(req)
      link=response.read()
      response.close()
      return link

def savefile(filename, contents,pastafinal=pastaperfil):
    try:
        destination = os.path.join(pastafinal,filename)
        fh = open(destination, 'wb')
        fh.write(contents)  
        fh.close()
    except: print "Nao gravou os temporarios de: %s" % filename

def openfile(filename,pastafinal=pastaperfil):
    try:
        destination = os.path.join(pastafinal, filename)
        fh = open(destination, 'rb')
        contents=fh.read()
        fh.close()
        return contents
    except:
        print "Nao abriu os temporarios de: %s" % filename
        return None


def abrir_url_cookie(url,erro=True):
      
      net.set_cookies(cookies)
      try:
            if status_lolabits:
               ref_data = {'Host': 'lolabits.es', 'Connection': 'keep-alive', 'Referer': 'http://lolabits.es/','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','User-Agent':user_agent,'Referer': 'http://abelhas.pt/'}            
            link=net.http_POST(url,ref_data).content.encode('latin-1','ignore')
            return link
      except urllib2.HTTPError, e:
            if erro==True: mensagemok('Lolabits.es',str(urllib2.HTTPError(e.url, e.code, traducao(40032), e.hdrs, e.fp)),traducao(40033))
            sys.exit(0)
      except urllib2.URLError, e:
            if erro==True: mensagemok('Lolabits.es',traducao(40032)+traducao(40033))
            sys.exit(0)

def versao_disponivel():
      try:
            link=abrir_url('http://fightnight-xbmc.googlecode.com/svn/addons/fightnight/plugin.video.abelhas/addon.xml')
            match=re.compile('name="Lolabits.es"\r\n       version="(.+?)"\r\n       provider-name="fightnight">').findall(link)[0]
      except:
            ok = mensagemok('Lolabits.es',traducao(40034),traducao(40035),'')
            match=traducao(40036)
      return match

def redirect(url):
      req = urllib2.Request(url)
      req.add_header('User-Agent', user_agent)
      response = urllib2.urlopen(req)
      gurl=response.geturl()
      return gurl

def get_params():
      param=[]
      paramstring=sys.argv[2]
      if len(paramstring)>=2:
            params=sys.argv[2]
            cleanedparams=params.replace('?','')
            if (params[len(params)-1]=='/'):
                  params=params[0:len(params)-2]
            pairsofparams=cleanedparams.split('&')
            param={}
            for i in range(len(pairsofparams)):
                  splitparams={}
                  splitparams=pairsofparams[i].split('=')
                  if (len(splitparams))==2:
                        param[splitparams[0]]=splitparams[1]                 
      return param

def clean(text):
      command={'\r':'','\n':'','\t':'','&nbsp;':' ','&quot;':'"','&amp;':'&','&ntilde;':'ñ','&#39;':'\'','&#170;':'ª','&#178;':'²','&#179;':'³','&#192;':'À','&#193;':'Á','&#194;':'Â','&#195;':'Ã','&#199;':'Ç','&#201;':'É','&#202;':'Ê','&#205;':'Í','&#211;':'Ó','&#212;':'Ó','&#213;':'Õ','&#217;':'Ù','&#218;':'Ú','&#224;':'à','&#225;':'á','&#226;':'â','&#227;':'ã','&#231;':'ç','&#232;':'è','&#233;':'é','&#234;':'ê','&#237;':'í','&#243;':'ó','&#244;':'ô','&#245;':'õ','&#249;':'ù','&#250;':'ú'}
      regex = re.compile("|".join(map(re.escape, command.keys())))
      return regex.sub(lambda mo: command[mo.group(0)], text)

#trailer,sn
def trailer(name, url):
    print name,url
    url = trailer2().run(name, url)
    if url == None: return
    item = xbmcgui.ListItem(path=url)
    item.setProperty("IsPlayable", "true")
    xbmc.Player().play(url, item)

class trailer2:
    def __init__(self):
        self.youtube_base = 'http://www.youtube.com'
        self.youtube_query = 'http://gdata.youtube.com/feeds/api/videos?q='
        self.youtube_watch = 'http://www.youtube.com/watch?v=%s'
        self.youtube_info = 'http://gdata.youtube.com/feeds/api/videos/%s?v=2'

    def run(self, name, url):
        try:
            if url.startswith(self.youtube_base):
                url = self.youtube(url)
                if url == None: raise Exception()
                return url
            elif not url.startswith('http://'):
                url = self.youtube_watch % url
                url = self.youtube(url)
                if url == None: raise Exception()
                return url
            else:
                raise Exception()
        except:
            url = self.youtube_query + name + ' trailer'
            url = self.youtube_search(url)
            if url == None: return
            return url

    def youtube_search(self, url):
        try:
            query = url.split("?q=")[-1].split("/")[-1].split("?")[0]
            url= url.split('[/B]')[0].replace('[B]','')
            url = url.replace(query, urllib.quote_plus(query))
            result = getUrl(url, timeout='10').result
            result = parseDOM(result, "entry")
            result = parseDOM(result, "id")

            for url in result[:5]:
                url = url.split("/")[-1]	
                url = self.youtube_watch % url
                url = self.youtube(url)
                if not url == None: return url
        except: return

    def youtube(self, url):
        print '#youtube'
        try:
            id = url.split("?v=")[-1].split("/")[-1].split("?")[0].split("&")[0]
            state, reason = None, None
            result = getUrl(self.youtube_info % id, timeout='10').result
            try:
                state = common.parseDOM(result, "yt:state", ret="name")[0]
                reason = common.parseDOM(result, "yt:state", ret="reasonCode")[0]
            except:
                pass
            if state == 'deleted' or state == 'rejected' or state == 'failed' or reason == 'requesterRegion' : return
            try:
                result = getUrl(self.youtube_watch % id, timeout='10').result
                alert = common.parseDOM(result, "div", attrs = { "id": "watch7-notification-area" })[0]
                return
            except:
                pass
            url = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % id
            return url
        except:
            return

class getUrl(object):
    def __init__(self, url, close=True, proxy=None, post=None, mobile=False, referer=None, cookie=None, output='', timeout='5'):
        if not proxy == None:
            proxy_handler = urllib2.ProxyHandler({'http':'%s' % (proxy)})
            opener = urllib2.build_opener(proxy_handler, urllib2.HTTPHandler)
            opener = urllib2.install_opener(opener)
        if output == 'cookie' or not close == True:
            import cookielib
            cookie_handler = urllib2.HTTPCookieProcessor(cookielib.LWPCookieJar())
            opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
            opener = urllib2.install_opener(opener)
        if not post == None:
            request = urllib2.Request(url, post)
        else:
            request = urllib2.Request(url,None)
        if mobile == True:
            request.add_header('User-Agent', 'Mozilla/5.0 (iPhone; CPU; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7')
        else:
            request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0')
        if not referer == None:
            request.add_header('Referer', referer)
        if not cookie == None:
            request.add_header('cookie', cookie)
        response = urllib2.urlopen(request, timeout=int(timeout))
        if output == 'cookie':
            result = str(response.headers.get('Set-Cookie'))
        elif output == 'geturl':
            result = response.geturl()
        else:
            result = response.read()
        if close == True:
            response.close()
        self.result = result

def parseDOM(html, name=u"", attrs={}, ret=False):
    if isinstance(name, str): # Should be handled
        try:  name = name #.decode("utf-8")
        except: pass

    if isinstance(html, str):
        try: html = [html.decode("utf-8")] # Replace with chardet thingy
        except: html = [html]
    elif isinstance(html, unicode): html = [html]
    elif not isinstance(html, list): return u""

    if not name.strip(): return u""

    ret_lst = []
    for item in html:
        temp_item = re.compile('(<[^>]*?\n[^>]*?>)').findall(item)
        for match in temp_item: item = item.replace(match, match.replace("\n", " "))

        lst = _getDOMElements(item, name, attrs)

        if isinstance(ret, str):
            lst2 = []
            for match in lst:
                lst2 += _getDOMAttributes(match, name, ret)
            lst = lst2
        else:
            lst2 = []
            for match in lst:
                temp = _getDOMContent(item, name, match, ret).strip()
                item = item[item.find(temp, item.find(match)) + len(temp):]
                lst2.append(temp)
            lst = lst2
        ret_lst += lst

    return ret_lst

def _getDOMContent(html, name, match, ret):  # Cleanup

    endstr = u"</" + name  # + ">"

    start = html.find(match)
    end = html.find(endstr, start)
    pos = html.find("<" + name, start + 1 )

    while pos < end and pos != -1:  # Ignore too early </endstr> return
        tend = html.find(endstr, end + len(endstr))
        if tend != -1:
            end = tend
        pos = html.find("<" + name, pos + 1)

    if start == -1 and end == -1:
        result = u""
    elif start > -1 and end > -1:
        result = html[start + len(match):end]
    elif end > -1:
        result = html[:end]
    elif start > -1:
        result = html[start + len(match):]

    if ret:
        endstr = html[end:html.find(">", html.find(endstr)) + 1]
        result = match + result + endstr

    return result

def _getDOMAttributes(match, name, ret):
    lst = re.compile('<' + name + '.*?' + ret + '=([\'"].[^>]*?[\'"])>', re.M | re.S).findall(match)
    if len(lst) == 0:
        lst = re.compile('<' + name + '.*?' + ret + '=(.[^>]*?)>', re.M | re.S).findall(match)
    ret = []
    for tmp in lst:
        cont_char = tmp[0]
        if cont_char in "'\"":

            # Limit down to next variable.
            if tmp.find('=' + cont_char, tmp.find(cont_char, 1)) > -1:
                tmp = tmp[:tmp.find('=' + cont_char, tmp.find(cont_char, 1))]

            # Limit to the last quotation mark
            if tmp.rfind(cont_char, 1) > -1:
                tmp = tmp[1:tmp.rfind(cont_char)]
        else:
            if tmp.find(" ") > 0:
                tmp = tmp[:tmp.find(" ")]
            elif tmp.find("/") > 0:
                tmp = tmp[:tmp.find("/")]
            elif tmp.find(">") > 0:
                tmp = tmp[:tmp.find(">")]

        ret.append(tmp.strip())

    return ret

def _getDOMElements(item, name, attrs):
    lst = []
    for key in attrs:
        lst2 = re.compile('(<' + name + '[^>]*?(?:' + key + '=[\'"]' + attrs[key] + '[\'"].*?>))', re.M | re.S).findall(item)
        if len(lst2) == 0 and attrs[key].find(" ") == -1:  # Try matching without quotation marks
            lst2 = re.compile('(<' + name + '[^>]*?(?:' + key + '=' + attrs[key] + '.*?>))', re.M | re.S).findall(item)

        if len(lst) == 0:
            lst = lst2
            lst2 = []
        else:
            test = range(len(lst))
            test.reverse()
            for i in test:  # Delete anything missing from the next list.
                if not lst[i] in lst2:
                    del(lst[i])

    if len(lst) == 0 and attrs == {}:
        lst = re.compile('(<' + name + '>)', re.M | re.S).findall(item)
        if len(lst) == 0:
            lst = re.compile('(<' + name + ' .*?>)', re.M | re.S).findall(item)

    return lst
#trailer,en

params=get_params()
url=None
name=None
mode=None
tamanhoparavariavel=None

try: url=urllib.unquote_plus(params["url"])
except: pass
try: tamanhoparavariavel=urllib.unquote_plus(params["tamanhof"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except: pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Name: "+str(tamanhoparavariavel)

if mode==None or url==None or len(url)<1:
      print "Versión Instalada: v" + version
      if selfAddon.getSetting('lolabits-enable') == 'false':
            ok = mensagemok('Lolabits','Precisa configurar el plugin','para poder acceder a los contenidos.')
            entrarnovamente(1)
      else:
            
            if selfAddon.getSetting('lolabits-enable') == 'true' and not selfAddon.getSetting('lolabits-username')== '':
                  if login_lolabits():
                        global status_abelhas
                        status_abelhas=True
                        selfAddon.setSetting('lolabits-check',"true")
                  else: selfAddon.setSetting('lolabits-check',"false")            
            menu_principal(1)
            
                  
elif mode==1: topcolecionadores()
elif mode==2: abelhasmaisrecentes(url)
elif mode==3: pastas(url,name)
elif mode==4: analyzer(url)
elif mode==5: caixadetexto(url)
elif mode==6: login_lolabits()
elif mode==7: pesquisa()
elif mode==8: selfAddon.openSettings()#sacarficheiros()
elif mode==9: favoritos()
elif mode==10: analyzer(url,subtitles='',playterm='playlist')
elif mode==11: analyzer(url,subtitles='',playterm='download')
elif mode==12: proxpesquisa_ab()
elif mode==13: comecarplaylist()
elif mode==14: limparplaylist()
elif mode==15: criarplaylist(url,name)
elif mode==16: obterlistadeficheiros()
elif mode==17: trailer(name, url)
elif mode==18: atalhos()
elif mode==19: atalhos(type='addfile')
elif mode==20: atalhos(type='addfolder')
elif mode==21: atalhos(type='remove')
elif mode==22: pastas('/'.join(url.split('/')[:-1]),name)
elif mode==23: pastas_de_fora(url,name)
elif mode==24: proxpesquisa_mt()
xbmcplugin.endOfDirectory(int(sys.argv[1]))
