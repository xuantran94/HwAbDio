#ifndef _HWABDIO_H_
#define _HWABDIO_H_

#include "HwAbDio_Cfg.h"

#if( STD_ON == HWABDIO_CFG_MODULE_ACTIVE )

void  HwAbDio_Init (void);
void  HwAbDio_Set (uint8 hwAbDioId_u8, uint8 state_u8);
void  HwAbDio_Get (uint8 hwAbDioId_u8, uint8* state_u8);


#if (HWABDIO_CFG_DEBUG == STD_ON)
#define HWABDIO_DEBUG(format, ...) ADP_LOG("HWABDIO", format, ## __VA_ARGS__ )
#else
#define HWABDIO_DEBUG(format, ...) 
#endif
#else

#define HwAbDio_Init()
#define HwAbDio_Set(x,y) 
#define HwAbDio_Get(x,y) 

#endif

#endif