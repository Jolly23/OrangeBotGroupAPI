# -*- coding: utf-8 -*-

ERRMSG = {
    -5: 'invalid api key',
    -2: 'information source server error',
    -1: 'information source server busy',
    0: 'ok',
    1: 'not found',
    2: 'invalid uid or password',

    -40001: 'APIMsgCryptCheck_MissQueryArgument_Error',
    -40002: 'APIMsgCryptCheck_MissBodyArgument_Error',
    -40003: 'APIMsgCryptCheck_NonceLength_Error',
    -40004: 'APIMsgCryptCheck_MessageSignature_Error',
    -40005: 'APIMsgCryptCheck_NoValidateAPIKey_Error',
    -40006: 'APIMsgCryptCheck_ArgsSignature_Error',
    -40007: 'APIMsgCryptCheck_ArgsType_Error',
    -40008: 'APIMsgCryptCheck_RequestArgs_Error',
    -40011: 'APIMsgCryptCheck_SHA1Check_Error',
    -40012: 'APIMsgCryptCheck_MsgDecryptOrSecretKey_Error',

    -40021: 'APIApplyCheck_NoPermittedMethod',
}

TIME_OUT = (1, 1)
