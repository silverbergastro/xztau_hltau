from ciao.contrib.runtool import *
from get_skycoords import get_skycoords


def extract_hltau(srcid,ra,dec):
    '''Extract TG spectrum for HL Tau from a given obs id. Inputs: srcid, ra, dec'''
    srcstring = str(srcid)
    
    
    #Set up dmcoords to get sky coordinates of source from RA and DEC
    dmcoords.punlearn()
    dmcoords.option = 'cel'
    dmcoords.ra = ra
    dmcoords.dec = dec
    
    #Get skycoords from RA and DEC
    testdmcoords = dmcoords(srcstring+'/repro/acisf'+srcstring+'_repro_evt2.fits',verbose=2)
    skyx, skyy = get_skycoords(testdmcoords)
    
    #Hard-code file names for future use
    evt1filename        = srcstring+'/secondary/acisf'+srcstring+'_000N002_evt1.fits'
    tgdetectoutfilename = srcstring+'/acis_'+srcstring+'_hltau.fits'
    maskfilename        = srcstring+'/acis_'+srcstring+'_hltau_evt1_L1a.fits'
    evt1afilename       = srcstring+'/acis_'+srcstring+'_hltau_evt1a.fits'
    filterfile1name     = srcstring+'/acis_'+srcstring+'_hltau_flt1_evt1a.fits'
    evt2filename        = srcstring+'/acis_'+srcstring+'_hltau_evt2.fits'
    
    #Use those coordinates to set up tgdetect2, then run tgdetect2
    tgdetect2.punlearn()
    tgdetect2.zo_pos_x = skyx
    tgdetect2.zo_pos_y = skyy
    tgdetect2.clobber = True
    tgdetect2.infile = evt1filename
    tgdetect2.outfile = tgdetectoutfilename
    tgdetect2.verbose = 2
    
    a = tgdetect2()
    print(a)
    
    tg_create_mask.punlearn()
    tg_create_mask.infile  = evt1filename
    tg_create_mask.outfile = maskfilename
    tg_create_mask.input_pos_tab = tgdetectourfilename
    tg_create_mask.verbose = 2
    tg_create_mask.clobber = True
    
    b = tg_create_mask()
    print(b)
    
    #tg_resolve_events
    tg_resolve_events.punlearn()
    tg_resolve_events.infile = evt1filename
    tg_resolve_events.outfile = evt1afilename
    tg_resolve_events.regionfile = maskfilename
    tg_resolve_events.acaofffile = srcstring+'/repro/pcadf'+srcstring+'_000N001_asol1.fits'
    tg_resolve_events.verbose = 2
    tg_resolve_events.clobber = True
    
    c = tg_resolve_events()
    print(c)
    
    #Filter events, first for grade and status
    dmcopy.punlearn()
    dmcopy.infile = evt1afilename+'[EVENTS][grade=0,2,3,4,6,status=0]'
    dmcopy.outfile = filterfile1name
    dmcopy.verbose = 2
    
    d = dmcopy()
    print(d)
    
    dmappend.punlearn()
    dmappend.infile = evt1afilename+'[region][subspace -time]'
    dmappend.outfile = filterfile1name
    
    d1 = dmappend()
    print(d1)
    
    #Second filter
    dmcopy.punlearn()
    dmcopy.infile = filterfile1name+'[EVENTS][@'+srcstring+'/secondary/acisf'+srcstring+'_000N002_flt1.fits][cols -phas]'
    dmcopy.outfile = evt2filename
    dmcopy.verbose = 2
    
    d2 = dmcopy()
    print(d2)
    
    dmappend.punlearn()
    
    dmappend.infile=evt1afilename+'[region][subspace -time]'
    dmappend.outfile = evt2filename
    dmappend.verbose = 2
    
    d3 = dmappend()
    print(d3)
    
    #tgextract
    tgextract.punlearn()
    tgextract.infile = evt2filename
    tgextract.outfile = srcstring+'/acis_'+srcstring+'_hltau_pha2.fits'
    tgextract.verbose = 2
    
    f = tgextract()
    print(f)
    print('\nDone')
    return