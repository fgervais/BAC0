#!/usr/bin/python
from ipy_progressbar import ProgressBar
import pandas as pd

def discoverPoints(bacnetapp,address, progress=True):
    pss = bacnetapp.read('%s device 5 protocolServicesSupported' % address)
    deviceName = bacnetapp.read('%s device 5 objectName' % address)
    print('Found %s' % deviceName)
    objList = bacnetapp.read('%s device 5 objectList' % address)
    result = []
    
    if progress:
        pb = ProgressBar(len(objList), title='Discovering points', key=objList)
        for i in pb:
            if objList[i][0] not in 'file calendar device schedule':
                if 'binary' not in objList[i][0] and 'multiState' not in objList[i][0]:
                    result.append(bacnetapp.readMultiple('%s %s %s objectName description presentValue units' % (address, objList[i][0], objList[i][1])))
                else:
                    result.append(bacnetapp.readMultiple('%s %s %s objectName description presentValue' % (address, objList[i][0], objList[i][1])))
    
    else:    
        for each in objList:
            if each[0] not in 'file calendar device schedule':
                if 'binary' not in each[0] and 'multiState' not in each[0]:
                    result.append(bacnetapp.readMultiple('%s %s %s objectName description presentValue units' % (address, each[0], each[1])))
                else:
                    result.append(bacnetapp.readMultiple('%s %s %s objectName description presentValue' % (address, each[0], each[1])))
    
            
    df = pd.DataFrame(result, columns=['name','description','presentValue','units']).set_index(['name'])
    return (deviceName,pss,objList,df)



