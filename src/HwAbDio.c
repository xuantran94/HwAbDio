#include "HwAbDio.h"
#if( STD_ON == HWABDIO_CFG_MODULE_ACTIVE )
#include "Dio.h"

void HwAbDio_Init (void)
{
    HWABDIO_DEBUG("Init");
};
void HwAbDio_Set (uint8 hwAbDioId_u8, uint8 state_u8)
{
    HWABDIO_DEBUG("Set %d to %d", hwAbDioId_u8, state_u8);
    hwAbDioDevConfig_ast[hwAbDioConfig_ast[hwAbDioId_u8].deviceId_u8]->Set_pfct(hwAbDioConfig_ast[hwAbDioId_u8].driverSignalId_u8, state_u8);
};
void HwAbDio_Get (uint8 hwAbDioId_u8, uint8* state_pu8)
{
    hwAbDioDevConfig_ast[hwAbDioConfig_ast[hwAbDioId_u8].deviceId_u8]->Get_pfct(hwAbDioConfig_ast[hwAbDioId_u8].driverSignalId_u8, state_pu8);
};
#endif