from typing import List
import objc
import CoreServices
import ApplicationServices
import struct

from AppKit import NSURL

from Foundation import NSBundle

def OSType(s):
    return int.from_bytes(s.encode("UTF-8"), "big")

event_manager = ApplicationServices.NSAppleEventManager.sharedAppleEventManager()

def send_event_to_bundle(event: int, bundle: str):
    app_desc = ApplicationServices.NSAppleEventDescriptor.alloc().initWithDescriptorType_data_(typeApplicationBundleID, bundle.encode("UTF-8"))

    new_event = ApplicationServices.NSAppleEventDescriptor.appleEventWithEventClass_eventID_targetDescriptor_returnID_transactionID_(typeAppleEvent, event, app_desc, kAutoGenerateReturnID, kAnyTransactionID)

    new_event.sendEventWithOptions_timeout_error_(kAEWaitReply|kAECanInteract, kAEDefaultTimeout, None)

def test():
    bundle = "com.apple.TextEdit"
    app_desc = ApplicationServices.NSAppleEventDescriptor.alloc().initWithDescriptorType_data_(typeApplicationBundleID, bundle.encode("UTF-8"))

    # event = ApplicationServices.NSAppleEventDescriptor.appleEventWithEventClass_eventID_targetDescriptor_returnID_transactionID_(kCoreEventClass, event, app_desc, kAutoGenerateReturnID, kAnyTransactionID)

    # file_desc = ApplicationServices.NSAppleEventDescriptor.alloc().initWithDescriptorType_data_(typeFileURL, "/".encode("UTF-8"))
    # event.setParamDescriptor_forKeyword_(file_desc, kAERevealSelection)

    #fileList = ApplicationServices.NSAppleEventDescriptor.listDescriptor()
    createEvent = ApplicationServices.NSAppleEventDescriptor.appleEventWithEventClass_eventID_targetDescriptor_returnID_transactionID_(kAECoreSuite, kAECreateElement, app_desc, kAutoGenerateReturnID, kAnyTransactionID)

    url = NSURL.alloc().initFileURLWithPath_("/Users/steven/Documents/blah.txt")
    desc = ApplicationServices.NSAppleEventDescriptor.alloc().initWithDescriptorType_data_(cDocument, url.absoluteString().encode("UTF-8"))
    #fileList.insertDescriptor_atIndex_(desc, 0)

    createEvent.setParamDescriptor_forKeyword_(desc, keyAEObjectClass)
    createEvent.sendEventWithOptions_timeout_error_(kAEWaitReply|kAECanInteract, kAEDefaultTimeout, None)

kAENoReply            =  1
kAENeverInteract      = 16
kAEDefaultTimeout     = -1
kAnyTransactionID     =  0
kAutoGenerateReturnID = -1

kAECanInteract        = 0x00000020
kAEWaitReply          = 0x00000003

typeAEList                    = OSType('list')
typeAERecord                  = OSType('reco')
typeEventRecord               = OSType('evrc')
typeAppleEvent                = OSType('aevt')
typeApplicationBundleID       = OSType('bund')
typeApplSignature             = OSType('sign')
typeFSRef                     = OSType('fsrf')
typeFileURL                   = OSType('furl')
typeApplicationURL            = OSType('aprl')
typeAppParameters             = OSType('appa')
typeTrue                      = OSType('true')
typeFalse                     = OSType('fals')
typeKernelProcessID           = OSType('kpid')
typeProcessSerialNumber       = OSType('psn ')
typeFixed                     = OSType('fixd')
typeBookmarkData              = OSType('bmrk')
typeWildCard                  = OSType('****')

kAEOpenApplication            = OSType('oapp')
kAEOpenDocuments              = OSType('odoc')
kAEPrintDocuments             = OSType('pdoc')
kAEOpenContents               = OSType('ocon')
kAEQuitApplication            = OSType('quit')
kAEAnswer                     = OSType('ansr')
kAEApplicationDied            = OSType('obit')
kAEShowPreferences            = OSType('pref')

keyDirectObject = OSType('----')

def xaevent_quit_application_by_bundle_id(bundle_id: str):
    send_event_to_bundle(kAEQuitApplication, "com.apple.MobileSMS")

cAEList                       = OSType('list')
cApplication                  = OSType('capp')
cArc                          = OSType('carc')
cBoolean                      = OSType('bool')
cCell                         = OSType('ccel')
cChar                         = OSType('cha ')
cColorTable                   = OSType('clrt')
cColumn                       = OSType('ccol')
cDocument                     = OSType('docu')
cDrawingArea                  = OSType('cdrw')
cEnumeration                  = OSType('enum')
cFile                         = OSType('file')
cFixed                        = OSType('fixd')
cFixedPoint                   = OSType('fpnt')
cFixedRectangle               = OSType('frct')
cGraphicLine                  = OSType('glin')
cGraphicObject                = OSType('cgob')
cGraphicShape                 = OSType('cgsh')
cGraphicText                  = OSType('cgtx')
cGroupedGraphic               = OSType('cpic')

cInsertionLoc                 = OSType('insl')
cInsertionPoint               = OSType('cins')
cIntlText                     = OSType('itxt')
cIntlWritingCode              = OSType('intl')
cItem                         = OSType('citm')
cLine                         = OSType('clin')
cLongDateTime                 = OSType('ldt ')
cLongFixed                    = OSType('lfxd')
cLongFixedPoint               = OSType('lfpt')
cLongFixedRectangle           = OSType('lfrc')
cLongInteger                  = OSType('long')
cLongPoint                    = OSType('lpnt')
cLongRectangle                = OSType('lrct')
cMachineLoc                   = OSType('mLoc')
cMenu                         = OSType('cmnu')
cMenuItem                     = OSType('cmen')
cObject                       = OSType('cobj')
cObjectSpecifier              = OSType('obj ')
cOpenableObject               = OSType('coob')
cOval                         = OSType('covl')

cParagraph                    = OSType('cpar')
cPICT                         = OSType('PICT')
cPixel                        = OSType('cpxl')
cPixelMap                     = OSType('cpix')
cPolygon                      = OSType('cpgn')
cProperty                     = OSType('prop')
cQDPoint                      = OSType('QDpt')
cQDRectangle                  = OSType('qdrt')
cRectangle                    = OSType('crec')
cRGBColor                     = OSType('cRGB')
cRotation                     = OSType('trot')
cRoundedRectangle             = OSType('crrc')
cRow                          = OSType('crow')
cSelection                    = OSType('csel')
cShortInteger                 = OSType('shor')
cTable                        = OSType('ctbl')
cText                         = OSType('ctxt')
cTextFlow                     = OSType('cflo')
cTextStyles                   = OSType('tsty')
cType                         = OSType('type')

cVersion                      = OSType('vers')
cWindow                       = OSType('cwin')
cWord                         = OSType('cwor')
enumArrows                    = OSType('arro')
enumJustification             = OSType('just')
enumKeyForm                   = OSType('kfrm')
enumPosition                  = OSType('posi')
enumProtection                = OSType('prtn')
enumQuality                   = OSType('qual')
enumSaveOptions               = OSType('savo')
enumStyle                     = OSType('styl')
enumTransferMode              = OSType('tran')
kAEAbout                      = OSType('abou')
kAEAfter                      = OSType('afte')
kAEAliasSelection             = OSType('sali')
kAEAllCaps                    = OSType('alcp')
kAEArrowAtEnd                 = OSType('aren')
kAEArrowAtStart               = OSType('arst')
kAEArrowBothEnds              = OSType('arbo')

kAEAsk                        = OSType('ask ')
kAEBefore                     = OSType('befo')
kAEBeginning                  = OSType('bgng')
kAEBeginsWith                 = OSType('bgwt')
kAEBeginTransaction           = OSType('begi')
kAEBold                       = OSType('bold')
kAECaseSensEquals             = OSType('cseq')
kAECentered                   = OSType('cent')
kAEChangeView                 = OSType('view')
kAEClone                      = OSType('clon')
kAEClose                      = OSType('clos')
kAECondensed                  = OSType('cond')
kAEContains                   = OSType('cont')
kAECopy                       = OSType('copy')
kAECoreSuite                  = OSType('core')
kAECountElements              = OSType('cnte')
kAECreateElement              = OSType('crel')
kAECreatePublisher            = OSType('cpub')
kAECut                        = OSType('cut ')
kAEDelete                     = OSType('delo')

kAEDoObjectsExist             = OSType('doex')
kAEDoScript                   = OSType('dosc')
kAEDrag                       = OSType('drag')
kAEDuplicateSelection         = OSType('sdup')
kAEEditGraphic                = OSType('edit')
kAEEmptyTrash                 = OSType('empt')
kAEEnd                        = OSType('end ')
kAEEndsWith                   = OSType('ends')
kAEEndTransaction             = OSType('endt')
kAEEquals                     = OSType('=   ')
kAEExpanded                   = OSType('pexp')
kAEFast                       = OSType('fast')
kAEFinderEvents               = OSType('FNDR')
kAEFormulaProtect             = OSType('fpro')
kAEFullyJustified             = OSType('full')
kAEGetClassInfo               = OSType('qobj')
kAEGetData                    = OSType('getd')
kAEGetDataSize                = OSType('dsiz')
kAEGetEventInfo               = OSType('gtei')
kAEGetInfoSelection           = OSType('sinf')

kAEGetPrivilegeSelection      = OSType('sprv')
kAEGetSuiteInfo               = OSType('gtsi')
kAEGreaterThan                = OSType('>   ')
kAEGreaterThanEquals          = OSType('>=  ')
kAEGrow                       = OSType('grow')
kAEHidden                     = OSType('hidn')
kAEHiQuality                  = OSType('hiqu')
kAEImageGraphic               = OSType('imgr')
kAEIsUniform                  = OSType('isun')
kAEItalic                     = OSType('ital')
kAELeftJustified              = OSType('left')
kAELessThan                   = OSType('<   ')
kAELessThanEquals             = OSType('<=  ')
kAELowercase                  = OSType('lowc')
kAEMakeObjectsVisible         = OSType('mvis')
kAEMiscStandards              = OSType('misc')
kAEModifiable                 = OSType('modf')
kAEMove                       = OSType('move')
kAENo                         = OSType('no  ')
kAENoArrow                    = OSType('arno')

# kAENonmodifiable
kAENonmodifiable              = OSType('nmod')
kAEOpen                       = OSType('odoc')
kAEOpenSelection              = OSType('sope')
kAEOutline                    = OSType('outl')
kAEPageSetup                  = OSType('pgsu')
kAEPaste                      = OSType('past')
kAEPlain                      = OSType('plan')
kAEPrint                      = OSType('pdoc')
kAEPrintSelection             = OSType('spri')
kAEPrintWindow                = OSType('pwin')
kAEPutAwaySelection           = OSType('sput')
kAEQDAddOver                  = OSType('addo')
kAEQDAddPin                   = OSType('addp')
kAEQDAdMax                    = OSType('admx')
kAEQDAdMin                    = OSType('admn')
kAEQDBic                      = OSType('bic ')
kAEQDBlend                    = OSType('blnd')
kAEQDCopy                     = OSType('cpy ')
kAEQDNotBic                   = OSType('nbic')
kAEQDNotCopy                  = OSType('ncpy')

# kAEQDNotOr
kAEQDNotOr                    = OSType('ntor')
kAEQDNotXor                   = OSType('nxor')
kAEQDOr                       = OSType('or  ')
kAEQDSubOver                  = OSType('subo')
kAEQDSubPin                   = OSType('subp')
kAEQDSupplementalSuite        = OSType('qdsp')
kAEQDXor                      = OSType('xor ')
kAEQuickdrawSuite             = OSType('qdrw')
kAEQuitAll                    = OSType('quia')
kAERedo                       = OSType('redo')
kAERegular                    = OSType('regl')
kAEReopenApplication          = OSType('rapp')
kAEReplace                    = OSType('rplc')
kAERequiredSuite              = OSType('reqd')
kAERevealSelection            = OSType('srev')
kAERevert                     = OSType('rvrt')
kAERightJustified             = OSType('rght')
kAESave                       = OSType('save')
kAESelect                     = OSType('slct')
kAESetData                    = OSType('setd')

# kAESetPosition
kAESetPosition                = OSType('posn')
kAEShadow                     = OSType('shad')
kAEShowClipboard              = OSType('shcl')
kAESmallCaps                  = OSType('smcp')
kAESpecialClassProperties     = OSType('c@#!')
kAEStrikethrough              = OSType('strk')
kAESubscript                  = OSType('sbsc')
kAESuperscript                = OSType('spsc')
kAETableSuite                 = OSType('tbls')
kAETextSuite                  = OSType('TEXT')
kAETransactionTerminated      = OSType('ttrm')
kAEUnderline                  = OSType('undl')
kAEUndo                       = OSType('undo')
kAEWholeWordEquals            = OSType('wweq')
kAEYes                        = OSType('yes ')
kAEZoom                       = OSType('zoom')

# kAELogOut
kAESleep                      = OSType('slep')
kAELogOut                     = OSType('logo')
kAEReallyLogOut               = OSType('rlgo')
kAEShutDown                   = OSType('shut')
kAEShowRestartDialog          = OSType('rrst')
kAEShowShutdownDialog         = OSType('rsdn')
kAERestart                    = OSType('rest')

def xaevent_sleep():
    send_event_to_bundle(kAESleep, "com.apple.loginwindow")

def xaevent_show_logout_dialog():
    send_event_to_bundle(kAELogOut, "com.apple.loginwindow")

def xaevent_logout_immediately():
    send_event_to_bundle(kAEReallyLogOut, "com.apple.loginwindow")

def xaevent_show_restart_dialog():
    send_event_to_bundle(kAEShowRestartDialog, "com.apple.loginwindow")

def xaevent_restart_immediately():
    send_event_to_bundle(kAERestart, "com.apple.loginwindow")

def xaevent_show_shutdown_dialog():
    send_event_to_bundle(kAEShowShutdownDialog, "com.apple.loginwindow")

def xaevent_shutdown_immediately():
    send_event_to_bundle(kAEShutDown, "com.apple.loginwindow")

# kAEMouseClass
kAEMouseClass                 = OSType('mous')
kAEDown                       = OSType('down')
kAEUp                         = OSType('up  ')
kAEMoved                      = OSType('move')
kAEStoppedMoving              = OSType('stop')
kAEWindowClass                = OSType('wind')
kAEUpdate                     = OSType('updt')
kAEActivate                   = OSType('actv')
kAEDeactivate                 = OSType('dact')
kAECommandClass               = OSType('cmnd')
kAEKeyClass                   = OSType('keyc')
kAERawKey                     = OSType('rkey')
kAEVirtualKey                 = OSType('keyc')
kAENavigationKey              = OSType('nave')
kAEAutoDown                   = OSType('auto')
kAEApplicationClass           = OSType('appl')
kAESuspend                    = OSType('susp')
kAEResume                     = OSType('rsme')
kAEDiskEvent                  = OSType('disk')
kAENullEvent                  = OSType('null')
kAEWakeUpEvent                = OSType('wake')
kAEScrapEvent                 = OSType('scrp')
kAEHighLevel                  = OSType('high')

keyAEAngle                    = OSType('kang')
keyAEArcAngle                 = OSType('parc')

keyAEBaseAddr                 = OSType('badd')
keyAEBestType                 = OSType('pbst')
keyAEBgndColor                = OSType('kbcl')
keyAEBgndPattern              = OSType('kbpt')
keyAEBounds                   = OSType('pbnd')
keyAECellList                 = OSType('kclt')
keyAEClassID                  = OSType('clID')
keyAEColor                    = OSType('colr')
keyAEColorTable               = OSType('cltb')
keyAECurveHeight              = OSType('kchd')
keyAECurveWidth               = OSType('kcwd')
keyAEDashStyle                = OSType('pdst')
keyAEData                     = OSType('data')
keyAEDefaultType              = OSType('deft')
keyAEDefinitionRect           = OSType('pdrt')
keyAEDescType                 = OSType('dstp')
keyAEDestination              = OSType('dest')
keyAEDoAntiAlias              = OSType('anta')
keyAEDoDithered               = OSType('gdit')
keyAEDoRotate                 = OSType('kdrt')

keyAEDoScale                  = OSType('ksca')
keyAEDoTranslate              = OSType('ktra')
keyAEEditionFileLoc           = OSType('eloc')
keyAEElements                 = OSType('elms')
keyAEEndPoint                 = OSType('pend')
keyAEEventClass               = OSType('evcl')
keyAEEventID                  = OSType('evti')
keyAEFile                     = OSType('kfil')
keyAEFileType                 = OSType('fltp')
keyAEFillColor                = OSType('flcl')
keyAEFillPattern              = OSType('flpt')
keyAEFlipHorizontal           = OSType('kfho')
keyAEFlipVertical             = OSType('kfvt')
keyAEFont                     = OSType('font')
keyAEFormula                  = OSType('pfor')
keyAEGraphicObjects           = OSType('gobs')
keyAEID                       = OSType('ID  ')
keyAEImageQuality             = OSType('gqua')
keyAEInsertHere               = OSType('insh')
keyAEKeyForms                 = OSType('keyf')

keyAEKeyword                  = OSType('kywd')
keyAELevel                    = OSType('levl')
keyAELineArrow                = OSType('arro')
keyAEName                     = OSType('pnam')
keyAENewElementLoc            = OSType('pnel')
keyAEObject                   = OSType('kobj')
keyAEObjectClass              = OSType('kocl')
keyAEOffStyles                = OSType('ofst')
keyAEOnStyles                 = OSType('onst')
keyAEParameters               = OSType('prms')
keyAEParamFlags               = OSType('pmfg')
keyAEPenColor                 = OSType('ppcl')
keyAEPenPattern               = OSType('pppa')
keyAEPenWidth                 = OSType('ppwd')
keyAEPixelDepth               = OSType('pdpt')
keyAEPixMapMinus              = OSType('kpmm')
keyAEPMTable                  = OSType('kpmt')
keyAEPointList                = OSType('ptlt')
keyAEPointSize                = OSType('ptsz')
keyAEPosition                 = OSType('kpos')

keyAEPropData                 = OSType('prdt')
keyAEProperties               = OSType('qpro')
keyAEProperty                 = OSType('kprp')
keyAEPropFlags                = OSType('prfg')
keyAEPropID                   = OSType('prop')
keyAEProtection               = OSType('ppro')
keyAERenderAs                 = OSType('kren')
keyAERequestedType            = OSType('rtyp')
keyAEResult                   = OSType('----')
keyAEResultInfo               = OSType('rsin')
keyAERotation                 = OSType('prot')
keyAERotPoint                 = OSType('krtp')
keyAERowList                  = OSType('krls')
keyAESaveOptions              = OSType('savo')
keyAEScale                    = OSType('pscl')
keyAEScriptTag                = OSType('psct')
keyAESearchText               = OSType('stxt')
keyAEShowWhere                = OSType('show')
keyAEStartAngle               = OSType('pang')
keyAEStartPoint               = OSType('pstp')
keyAEStyles                   = OSType('ksty')

keyAESuiteID                  = OSType('suit')
keyAEText                     = OSType('ktxt')
keyAETextColor                = OSType('ptxc')
keyAETextFont                 = OSType('ptxf')
keyAETextPointSize            = OSType('ptps')
keyAETextStyles               = OSType('txst')
keyAETextLineHeight           = OSType('ktlh')
keyAETextLineAscent           = OSType('ktas')
keyAETheText                  = OSType('thtx')
keyAETransferMode             = OSType('pptm')
keyAETranslation              = OSType('ptrs')
keyAETryAsStructGraf          = OSType('toog')
keyAEUniformStyles            = OSType('ustl')
keyAEUpdateOn                 = OSType('pupd')
keyAEUserTerm                 = OSType('utrm')
keyAEWindow                   = OSType('wndw')
keyAEWritingCode              = OSType('wrcd')

keyMiscellaneous              = OSType('fmsc')
keySelection                  = OSType('fsel')
keyWindow                     = OSType('kwnd')
keyWhen                       = OSType('when')
keyWhere                      = OSType('wher')
keyModifiers                  = OSType('mods')
keyKey                        = OSType('key ')
keyKeyCode                    = OSType('code')
keyKeyboard                   = OSType('keyb')
keyDriveNumber                = OSType('drv#')
keyErrorCode                  = OSType('err#')
keyHighLevelClass             = OSType('hcls')
keyHighLevelID                = OSType('hid ')

pArcAngle                     = OSType('parc')
pBackgroundColor              = OSType('pbcl')
pBackgroundPattern            = OSType('pbpt')
pBestType                     = OSType('pbst')
pBounds                       = OSType('pbnd')
pClass                        = OSType('pcls')
pClipboard                    = OSType('pcli')
pColor                        = OSType('colr')
pColorTable                   = OSType('cltb')
pContents                     = OSType('pcnt')
pCornerCurveHeight            = OSType('pchd')
pCornerCurveWidth             = OSType('pcwd')
pDashStyle                    = OSType('pdst')
pDefaultType                  = OSType('deft')
pDefinitionRect               = OSType('pdrt')
pEnabled                      = OSType('enbl')
pEndPoint                     = OSType('pend')
pFillColor                    = OSType('flcl')
pFillPattern                  = OSType('flpt')
pFont                         = OSType('font')

pFormula                      = OSType('pfor')
pGraphicObjects               = OSType('gobs')
pHasCloseBox                  = OSType('hclb')
pHasTitleBar                  = OSType('ptit')
pID                           = OSType('ID  ')
pIndex                        = OSType('pidx')
pInsertionLoc                 = OSType('pins')
pIsFloating                   = OSType('isfl')
pIsFrontProcess               = OSType('pisf')
pIsModal                      = OSType('pmod')
pIsModified                   = OSType('imod')
pIsResizable                  = OSType('prsz')
pIsStationeryPad              = OSType('pspd')
pIsZoomable                   = OSType('iszm')
pIsZoomed                     = OSType('pzum')
pItemNumber                   = OSType('itmn')
pJustification                = OSType('pjst')
pLineArrow                    = OSType('arro')
pMenuID                       = OSType('mnid')
pName                         = OSType('pnam')

pNewElementLoc                = OSType('pnel')
pPenColor                     = OSType('ppcl')
pPenPattern                   = OSType('pppa')
pPenWidth                     = OSType('ppwd')
pPixelDepth                   = OSType('pdpt')
pPointList                    = OSType('ptlt')
pPointSize                    = OSType('ptsz')
pProtection                   = OSType('ppro')
pRotation                     = OSType('prot')
pScale                        = OSType('pscl')
pScript                       = OSType('scpt')
pScriptTag                    = OSType('psct')
pSelected                     = OSType('selc')
pSelection                    = OSType('sele')
pStartAngle                   = OSType('pang')
pStartPoint                   = OSType('pstp')
pTextColor                    = OSType('ptxc')
pTextFont                     = OSType('ptxf')
pTextItemDelimiters           = OSType('txdl')
pTextPointSize                = OSType('ptps')

pTextStyles                   = OSType('txst')
pTransferMode                 = OSType('pptm')
pTranslation                  = OSType('ptrs')
pUniformStyles                = OSType('ustl')
pUpdateOn                     = OSType('pupd')
pUserSelection                = OSType('pusl')
pVersion                      = OSType('vers')
pVisible                      = OSType('pvis')

typeAEText                    = OSType('tTXT')
typeArc                       = OSType('carc')
typeBest                      = OSType('best')
typeCell                      = OSType('ccel')
typeClassInfo                 = OSType('gcli')
typeColorTable                = OSType('clrt')
typeColumn                    = OSType('ccol')
typeDashStyle                 = OSType('tdas')
typeData                      = OSType('tdta')
typeDrawingArea               = OSType('cdrw')
typeElemInfo                  = OSType('elin')
typeEnumeration               = OSType('enum')
typeEPS                       = OSType('EPS ')
typeEventInfo                 = OSType('evin')

typeFinderWindow              = OSType('fwin')
typeFixedPoint                = OSType('fpnt')
typeFixedRectangle            = OSType('frct')
typeGraphicLine               = OSType('glin')
typeGraphicText               = OSType('cgtx')
typeGroupedGraphic            = OSType('cpic')
typeInsertionLoc              = OSType('insl')
typeIntlText                  = OSType('itxt')
typeIntlWritingCode           = OSType('intl')
typeLongDateTime              = OSType('ldt ')
typeCFAbsoluteTime            = OSType('cfat')
typeISO8601DateTime           = OSType('isot')
typeLongFixed                 = OSType('lfxd')
typeLongFixedPoint            = OSType('lfpt')
typeLongFixedRectangle        = OSType('lfrc')
typeLongPoint                 = OSType('lpnt')
typeLongRectangle             = OSType('lrct')
typeMachineLoc                = OSType('mLoc')
typeOval                      = OSType('covl')
typeParamInfo                 = OSType('pmin')
typePict                      = OSType('PICT')

typePixelMap                  = OSType('cpix')
typePixMapMinus               = OSType('tpmm')
typePolygon                   = OSType('cpgn')
typePropInfo                  = OSType('pinf')
typePtr                       = OSType('ptr ')
typeQDPoint                   = OSType('QDpt')
typeQDRegion                  = OSType('Qrgn')
typeRectangle                 = OSType('crec')
typeRGB16                     = OSType('tr16')
typeRGB96                     = OSType('tr96')
typeRGBColor                  = OSType('cRGB')
typeRotation                  = OSType('trot')
typeRoundedRectangle          = OSType('crrc')
typeRow                       = OSType('crow')
typeScrapStyles               = OSType('styl')
typeScript                    = OSType('scpt')
typeStyledText                = OSType('STXT')
typeSuiteInfo                 = OSType('suin')
typeTable                     = OSType('ctbl')
typeTextStyles                = OSType('tsty')

typeTIFF                      = OSType('TIFF')
typeJPEG                      = OSType('JPEG')
typeGIF                       = OSType('GIFf')
typeVersion                   = OSType('vers')

kAEMenuClass                  = OSType('menu')
kAEMenuSelect                 = OSType('mhit')
kAEMouseDown                  = OSType('mdwn')
kAEMouseDownInBack            = OSType('mdbk')
kAEKeyDown                    = OSType('kdwn')
kAEResized                    = OSType('rsiz')
kAEPromise                    = OSType('prom')

keyMenuID                     = OSType('mid ')
keyMenuItem                   = OSType('mitm')
keyCloseAllWindows            = OSType('caw ')
keyOriginalBounds             = OSType('obnd')
keyNewBounds                  = OSType('nbnd')
keyLocalWhere                 = OSType('lwhr')

typeHIMenu                    = OSType('mobj')
typeHIWindow                  = OSType('wobj')

kAEQuitReason                 = OSType('why?')

kBySmallIcon                  = 0
kByIconView                   = 1
kByNameView                   = 2
kByDateView                   = 3
kBySizeView                   = 4
kByKindView                   = 5
kByCommentView                = 6
kByLabelView                  = 7
kByVersionView                = 8

def xaevent_open_items_at_paths(paths: List[str]):
    app_desc = ApplicationServices.NSAppleEventDescriptor.alloc().initWithDescriptorType_data_(typeApplicationBundleID, "com.apple.Finder".encode("UTF-8"))

    fileList = ApplicationServices.NSAppleEventDescriptor.listDescriptor()
    openEvent = ApplicationServices.NSAppleEventDescriptor.appleEventWithEventClass_eventID_targetDescriptor_returnID_transactionID_(typeAppleEvent, kAEOpenDocuments, app_desc, kAutoGenerateReturnID, kAnyTransactionID)

    for path in paths:
        url = NSURL.alloc().initFileURLWithPath_(path)
        desc = ApplicationServices.NSAppleEventDescriptor.alloc().initWithDescriptorType_data_(typeFileURL, url.absoluteString().encode("UTF-8"))
        fileList.insertDescriptor_atIndex_(desc, 0)

    openEvent.setParamDescriptor_forKeyword_(fileList, keyDirectObject)
    openEvent.sendEventWithOptions_timeout_error_(kAEWaitReply|kAECanInteract, kAEDefaultTimeout, None)