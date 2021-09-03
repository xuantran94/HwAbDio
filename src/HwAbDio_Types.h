#ifndef _HWABDIO_TYPES_H_
#define _HWABDIO_TYPES_H_

#include "Std_Types.h"

typedef struct
{
    const uint8                     deviceId_u8;
    const uint8                     driverSignalId_u8;
}hwAbDioConfig_tst;

typedef struct
{
    Std_ReturnType (*Get_pfct)(uint8 idSignal_u8, uint8 *stSignal_pu8);
    Std_ReturnType (*Set_pfct)(uint8 idSignal_u8, uint8 stSignal_u8);
} hwAbDio_DeviceInterface_tst;

#endif