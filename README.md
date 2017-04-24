# WX-GROUP-API

<!-- TOC depthFrom:1 depthTo:6 withLinks:1 updateOnSave:1 orderedList:0 -->

- [WX-GROUP-API](#wx-group-api)
- [项目介绍](#项目介绍)
- [接口文档](#接口文档)
	- [全局返回码（errcode）说明](#全局返回码errcode说明)
	- [接口密钥 API_KEY 及 SECRET_KEY 说明](#接口密钥-apikey-及-secretkey-说明)
	- [API 请求数据 及 加密方式](#api-请求数据-及-加密方式)
		- [1\. `请求所需数据`准备](#1-请求所需数据准备)
		- [2\. `args_sign`算法](#2-argssign算法)
			- [2.1 第一步 生成11-32位任意长度的随机字符串nonce](#21-第一步-生成11-32位任意长度的随机字符串nonce)
			- [2.2 第二步 将请求所需json数据 结合 nonce 进行签名 生成 args_sign](#22-第二步-将请求所需json数据-结合-nonce-进行签名-生成-argssign)
		- [3\. `加密消息体encrypt_msg`算法](#3-加密消息体encryptmsg算法)
		- [4\. `请求数据签名msg_signature`算法](#4-请求数据签名msgsignature算法)
		- [5\. 调用API方法](#5-调用api方法)
			- [5.1 在url上携带参数](#51-在url上携带参数)
			- [5.2 POST方法携带的参数](#52-post方法携带的参数)
	- [微信机器人列表](#微信机器人列表)
		- [1\. 新增微信机器人](#1-新增微信机器人)
			- [1.1 请求参数说明](#11-请求参数说明)
			- [1.2 data返回参数说明](#12-data返回参数说明)
		- [2\. 停用机器人](#2-停用机器人)
			- [2.1 请求参数说明](#21-请求参数说明)
			- [2.2 data返回参数说明](#22-data返回参数说明)
		- [3\. 复通已停止使用的机器人](#3-复通已停止使用的机器人)
			- [3.1 请求参数说明](#31-请求参数说明)
			- [3.2 data返回参数说明](#32-data返回参数说明)
		- [4\. 修改机器人信息](#4-修改机器人信息)
			- [4.1 请求参数说明](#41-请求参数说明)
			- [4.2 data返回参数说明](#42-data返回参数说明)
		- [5\. 查找机器人](#5-查找机器人)
			- [5.1 请求参数说明](#51-请求参数说明)
			- [5.2 data返回参数说明](#52-data返回参数说明)
		- [6\. 获取当前全部机器人](#6-获取当前全部机器人)
			- [6.1 请求参数说明](#61-请求参数说明)
			- [6.2 data返回参数说明](#62-data返回参数说明)
		- [7\. 删除机器人](#7-删除机器人)
			- [7.1 请求参数说明](#71-请求参数说明)
			- [7.2 data返回参数说明](#72-data返回参数说明)
	- [微信群列表管理](#微信群列表管理)
		- [1\. 新增微信群信息](#1-新增微信群信息)
			- [1.1 请求参数说明](#11-请求参数说明)
			- [1.2 data返回参数说明](#12-data返回参数说明)
		- [2\. 微信群停止展示](#2-微信群停止展示)
			- [2.1 请求参数说明](#21-请求参数说明)
			- [2.2 data返回参数说明](#22-data返回参数说明)
		- [3\. 微信群恢复展示](#3-微信群恢复展示)
			- [3.1 请求参数说明](#31-请求参数说明)
			- [3.2 data返回参数说明](#32-data返回参数说明)
		- [4\. 微信群恢复展示](#4-微信群恢复展示)
			- [4.1 请求参数说明](#41-请求参数说明)
			- [4.2 data返回参数说明](#42-data返回参数说明)
		- [5\. 微信群信息修改](#5-微信群信息修改)
			- [5.1 请求参数说明](#51-请求参数说明)
			- [5.2 data返回参数说明](#52-data返回参数说明)

<!-- /TOC -->

# 项目介绍

基于`Tornado`框架的数据接口平台

# 接口文档

--------------------------------------------------------------------------------

## 全局返回码（errcode）说明

返回码 | 说明
--- | --------------
-2  | 服务器出错
-1  | 服务器忙
0   | 成功
1   | 页面不存在，请求缺少必要参数
2   | 用户名或密码验证失败
-40002   | APIMsgCryptCheck_MissQueryArgument_Error
-40003   | APIMsgCryptCheck_MissBodyArgument_Error
-40004   | APIMsgCryptCheck_MessageSignature_Error
-40005   | APIMsgCryptCheck_NoValidateAPIKey_Error
-40006   | APIMsgCryptCheck_ArgsSignature_Error
-40007   | APIMsgCryptCheck_ArgsType_Error
-40008   | APIMsgCryptCheck_MissCompulsoryArgs_Error
-40011   | APIMsgCryptCheck_SHA1Check_Error
-40012   | APIMsgCryptCheck_MsgDecryptOrSecretKey_Error
-40021   | APIApplyCheck_NoPermittedMethod



## 接口密钥 API_KEY 及 SECRET_KEY 说明

API-KEY 为 WX-GROUP-API 发放的 为实现数据加解密和识别接口调用者所使用的字符串，使用接口必须按照要求提交密钥进行验证，密钥错误或者未携带密钥将拒绝提供数据，申请密钥请发送邮件至zhaolei@protonmail.com

## API 请求数据 及 加密方式

URL携带参数  | 是否必须 | 说明
--- | ---- | ---
timestamp | 是    | 精确到秒的时间戳
nonce     | 是    | 随机字符串
msg_signature | 是    | `请求数据签名`（body + query）


POST参数  | 是否必须 | 说明
--- | ---- | ---
encrypt_msg | 是    | `加密消息体`
args_sign | 是    | `消息签名`
api_key | 是    | API_KEY

### 1\. `请求所需数据`准备
将所需数据名及所需数据列入Json中
例如：教务个人详细信息查询
```json
{
    "uid": "2014131126",
    "passwd": "123456"
}
```

### 2\. `args_sign`算法
#### 2.1 第一步 生成11-32位任意长度的随机字符串nonce
#### 2.2 第二步 将请求所需json数据 结合 nonce 进行签名 生成 args_sign
签名生成的通用步骤如下：

第一步，设所有发送或者接收到的数据为集合M，将集合M内非空参数值的参数按照参数名ASCII码从小到大排序（字典序），使用URL键值对的格式（即key1=value1&key2=value2…）拼接成字符串stringA。

特别注意以下重要规则：

◆ 参数名ASCII码从小到大排序（字典序）；

◆ 如果参数的值为空不参与签名；

◆ 参数名区分大小写；

◆ 如果访问无需参数，请给'{}'，签名；

第二步，在stringA最后拼接上string得到stringSignTemp字符串，并对stringSignTemp进行MD5运算，再将得到的字符串所有字符转换为大写，得到sign值signValue。

string = nonce

举例：

假设传送的参数如下：

```json
{
    "uid": "2014131126",
    "passwd": "123456"
}
```

第一步：对参数按照key=value的格式，并按照参数名ASCII字典序排序如下：

stringA="passwd=123456&uid=2014131126";

第二步：拼接string字符串：

假设第一步生成的随机字符串nonce="wad889dWDWAdiwaodadNWDJ"

stringSignTemp=stringA+"&string=wad889dWDWAdiwaodadNWDJ"

args_sign=MD5(stringSignTemp).toUpperCase()="9955408C48C1C9A92AA6049AEE6FFAE9"

特别注意：如果调用的API功能不需要参数（例如获取新闻不带参数则默认第一页）

stringSignTemp="&string="wad889dWDWAdiwaodadNWDJ"

### 3\. `加密消息体encrypt_msg`算法
采用AES对称加密算法（AES/CBC/ZeroPadding 128位模式）为调用接口所需要的参数进行加密 生成 encrypt_msg

AES密钥  | 值
--- | ----
KEY | SECRET_KEY 的 16位MD5值
IV | args_sign 的 16位MD5值

假设传送的参数如下：

```json
{
    "uid": "2014131126",
    "passwd": "123456"
}
```
假设API-KEY 对应的 SECRET_KEY 为 JSZqvCElb16pqZc1l4tmdOrOiK27ppH6tO1oABhpWxbJoIH4PDMRKXjc8Omwea5UtQo

此参数在第二步生成的 args_sign 为 9955408C48C1C9A92AA6049AEE6FFAE9

最后生成的结果encrypt_msg将为 c5ae0f4c2dddd64e303d27d56591c59f04d14371ac77acf76d1f65b8cd284e3058ec3dbb154b500569963a498934ac12



### 4\. `请求数据签名msg_signature`算法

为url和body中携带的nonce, str(timestamp), encrypt_msg, args_sign, api_key参数进行排序后求sha1的大写值：

将nonce, str(timestamp), encrypt_msg, args_sign, api_key五个参数进行字典序排序

将五个参数字符串拼接成一个字符串进行sha1加密后转换大写，生成msg_signature


### 5\. 调用API方法

#### 5.1 在url上携带参数

timestamp秒时间戳, `args_sign`算法中第一步生成的nonce, `请求数据签名msg_signature`算法中生成的msg_signature

注意：timestamp在整个加密&请求过程中需保持一致

#### 5.2 POST方法携带的参数

`加密消息体encrypt_msg`算法中生成的encrypt_msg, `args_sign`算法中生成的args_sign, 接口api_key

示例：以post的形式请求：<http://api.xxx.com/api/xxx>
```python
import requests
requests.post(
    url="http://api.xxx.com/api/xxx",
    parame={
        'nonce': 'YOvmnLpUw1p3faRoQUg0qW689',
        'timestamp': '1491395776',
        'msg_signature': '7B73CF91740D1420B1618920E52A01238BEAFB60'
    },
    data={
        'encrypt_msg': 'uwaduwaduuuUDW98awdadwDWAD9WADAWjawdua',
        'args_sign': 'JKJIOJGTFVCBHMNPLOTSETGUXHSKM',
        'api-key': 'xxxx'
    }
)
```

## 微信机器人列表

### 1\. 新增微信机器人

接口调用请求说明

> 新增微信机器人


http请求方式：Post <http://api.xxx.com/api/new_bot>


#### 1.1 请求参数说明

加密消息参数  | 是否必须 | 说明
--- | ---- | ---
bot_name | 是    | 机器人名
wx_id | 是    | 机器人微信号
base64_qrcode | 是    | 机器人二维码
expire_date | 否    | 此机器人信息过期时间（可无）
remark | 否    | 备注信息

返回结果 正确时的返回JSON数据包如下：

```json
{
    "errcode":0,
    "errmsg":"ok",
    "data":{
            "bot_name": "Ai dog",
            "wx_id": "xxxxxx",
            "create_date": "2017-04-24",
            "expire_date": "2018-04-24",
            "status": 0
        }
}
```

错误时的返回JSON数据包如下（示例为wx_id重复）：

```json
{
    "errcode":-30002,
    "errmsg":"wx_id already exist"
}
```

#### 1.2 data返回参数说明

参数          | 是否必须 | 说明
----------- | ---- | ---------------------
bot_name  | 否    | Str 机器人名
wx_id  | 否    | Str 微信id
create_date | 否    | Str 此机器人信息创建时间 `2017-04-23`
expire_date | 否    | Str 此机器人信息失效时间 `2018-01-01`
status | 否    | Int 机器人状态码


### 2\. 停用机器人

接口调用请求说明

> 停用机器人将会 立即停止 展示此微信机器人管理的群，此机器人状态将变为停用

http请求方式：Post <http://api.mindaxiaosi.com/api/turn_off_bot>

#### 2.1 请求参数说明

加密消息参数  | 是否必须 | 说明
--- | ---- | --
wx_id | 是    | 机器人微信号

返回结果 正确时的返回JSON数据包如下：

```json
{
    "errcode":0,
    "errmsg":"ok",
    "data": {
            "bot_name": "Ai dog",
            "wx_id": "xxxxxx",
            "status": -30001
        }
}
```

错误时的返回JSON数据包如下（示例为wx_id未找到）：

```json
{
    "errcode":-30002,
    "errmsg":"wx_id not found"
}
```

#### 2.2 data返回参数说明

参数         | 是否必须 | 说明
---------- | ---- | --------------------
bot_name | 否    | Str 机器人名
wx_id     | 否    | Str 微信id
status     | 否    | Int `-30001 机器人停用状态`


### 3\. 复通已停止使用的机器人

接口调用请求说明

> 开通当前停用的一个机器人，立即开始 展示此微信机器人管理的群，此机器人状态将变为正常

http请求方式：Post <http://api.mindaxiaosi.com/api/reopen_bot>

#### 3.1 请求参数说明

加密消息参数  | 是否必须 | 说明
--- | ---- | --
wx_id | 是    | 机器人微信号

返回结果 正确时的返回JSON数据包如下：

```json
{
    "errcode":0,
    "errmsg":"ok",
    "data": {
            "bot_name": "Ai dog",
            "wx_id": "xxxxxx",
            "status": 0
        }
}
```

错误时的返回JSON数据包如下（示例为当前wx_id机器人为正常使用状态，无法进行复通操作）：

```json
{
    "errcode":-30002,
    "errmsg":"bot in service"
}
```

#### 3.2 data返回参数说明

参数         | 是否必须 | 说明
---------- | ---- | --------------------
bot_name | 否    | Str 机器人名
wx_id     | 否    | Str 微信id
status     | 否    | Int `0 机器人正常状态`


### 4\. 修改机器人信息

接口调用请求说明

> 修改机器人信息，提交信息与创建机器人类似，但此功能无法用于创建新机器人，并且不能通过此修改机器人状态

http请求方式：Post <http://api.mindaxiaosi.com/api/modify_bot>

#### 4.1 请求参数说明

加密消息参数  | 是否必须 | 说明
--- | ---- | --
wx_id | 是    | 机器人微信号（不支持修改）
name | 否（修改则带此参数）    | 机器人名
base64_qrcode | 否（修改则带此参数）    | 机器人二维码
expire_date | 否（修改则带此参数）    | 此机器人信息过期时间（可无）
remark | 否（修改则带此参数）    | 备注信息（可无）


返回结果 正确时的返回JSON数据包如下：

```json
{
    "errcode":0,
    "errmsg":"ok",
    "data": {
            "bot_name": {
              "new": "Ai puppy",
              "old": "Ai dog"
            },
            "base64_qrcode": {
              "new": "ihuadwadiwauidwauihudawuhidhuawuhduhawuhduhwahudwauhduhwau...",
              "old": "oiwioiqouiwqiaiioaijodoamkxmkakkldmkwaodoawodopwaopdoawooo..."
            },
            "expire_date": {
              "new": "2019-04-24",
              "old": "2018-04-24"
            },
            "remark": {
              "new": "xxx修改",
              "old": "小桔创建"
            },
            "status": 0
        }
}
```

错误时的返回JSON数据包如下（示例为wx_id未找到）：

```json
{
    "errcode":-30002,
    "errmsg":"wx_id not found"
}
```

#### 4.2 data返回参数说明

参数         | 是否必须 | 说明
---------- | ---- | --------------------
bot_name  | 否（被改将展示）    | Str 机器人名
base64_qrcode | 否（被改将展示）    | Str 此机器人二维码base64
expire_date | 否（被改将展示）    | Str 此机器人信息失效时间 `2018-01-01`
remark | 否（被改将展示）    | Str 备注
status | 否    | Int 机器人状态码


### 5\. 查找机器人

接口调用请求说明

> 通过 微信名／微信id／二维码查找机器人

http请求方式：Post <http://api.mindaxiaosi.com/api/search_bot>

#### 5.1 请求参数说明

加密消息参数  | 是否必须 | 说明
--- | ---- | --
wx_id | 参数三选一即可    | 机器人微信号
name | 参数三选一即可    | 机器人名
base64_qrcode | 参数三选一即可    | 机器人二维码


返回结果 正确时的返回JSON数据包如下：

```json
{
    "errcode":0,
    "errmsg":"ok",
    "data": {
            "bot_name": "Ai dog",
            "wx_id": "xxxxxx",
            "create_date": "2017-04-24",
            "expire_date": "2018-04-24",
            "status": 0
        }
}
```

错误时的返回JSON数据包如下（示例为wx_id未找到）：

```json
{
    "errcode":-30002,
    "errmsg":"wx_id not found"
}
```

#### 5.2 data返回参数说明

参数         | 是否必须 | 说明
---------- | ---- | --------------------
bot_name  | 否    | Str 机器人名
wx_id  | 否    | Str 微信id
create_date | 否    | Str 此机器人信息创建时间 `2017-04-23`
expire_date | 否    | Str 此机器人信息失效时间 `2018-01-01`
status | 否    | Int 机器人状态码
remark | 否    | Str 备注信息


### 6\. 获取当前全部机器人

接口调用请求说明

> 获取当前全部机器人

http请求方式：Post <http://api.mindaxiaosi.com/api/all_bot>

#### 6.1 请求参数说明

加密消息参数  | 是否必须 | 说明
--- | ---- | --
qrcode | 否    | 返回数据是否携带二维码，默认为`n`不带（信息长度小），`y`携带base64二维码（数据大）


返回结果 正确时的返回JSON数据包如下：

```json
{
    "errcode":0,
    "errmsg":"ok",
    "data":[
        {
            "bot_name": "Ai dog",
            "wx_id": "xxxxxx",
            "base64_qrcode": "ihuadwadiwauidwauihudawuhidhuawuhduhawuhduhwahudwauhduhwau...",
            "create_date": "2017-04-24",
            "expire_date": "2018-04-24",
            "remark": "小桔创建",
            "status": 0
        },
        {
            "bot_name": "Orange dog",
            "wx_id": "orange_xxx",
            "base64_qrcode": "ihuadwadiwauidwauihudawuhidhuawuhduhawuhduhwahudwauhduhwau...",
            "create_date": "2017-04-24",
            "expire_date": null,
            "remark": "小桔创建",
            "status": 0
        },
        {
            "bot_name": "Jolly dog",
            "wx_id": "jolly_puppy",
            "base64_qrcode": "ihuadwadiwauidwauihudawuhidhuawuhduhawuhduhwahudwauhduhwau...",
            "create_date": "2017-04-24",
            "expire_date": null,
            "remark": "小桔创建",
            "status": -30001
        }
    ]
}
```

错误时的返回JSON数据包如下（示例为API系统发生故障）：

```json
{
    "errcode":-2,
    "errmsg":"server error"
}
```

#### 6.2 data返回参数说明

参数         | 是否必须 | 说明
---------- | ---- | --------------------
bot_name  | 否    | Str 机器人名
wx_id | 否    | Str 机器人微信号
base64_qrcode | 否    | Str 机器人二维码
create_date | 否    | Str 此机器人信息创建时间 `2017-04-23`
expire_date | 否    | Str 此机器人信息创建时间 `2017-04-23`
remark | 否    | 备注信息
status | 否    | Int 机器人状态码


### 7\. 删除机器人

接口调用请求说明

> 删除某个机器人，将立即停止显示其全部管理中的群，并且在全部机器人列表中消失

http请求方式：Post <http://api.mindaxiaosi.com/api/del_bot>

#### 7.1 请求参数说明

加密消息参数  | 是否必须 | 说明
--- | ---- | --
wx_id | 是    | 机器人微信号


返回结果 正确时的返回JSON数据包如下：

```json
{
    "errcode":0,
    "errmsg":"ok",
    "data":{
            "bot_name": "Ai dog",
            "wx_id": "xxxxxx",
            "base64_qrcode": "ihuadwadiwauidwauihudawuhidhuawuhduhawuhduhwahudwauhduhwau...",
            "create_date": "2017-04-24",
            "expire_date": "2018-04-24",
            "remark": "小桔创建",
            "status": -401
        }
}
```

错误时的返回JSON数据包如下（示例为wx_id未找到）：

```json
{
    "errcode":-30002,
    "errmsg":"wx_id not found"
}
```

#### 7.2 data返回参数说明

参数         | 是否必须 | 说明
---------- | ---- | --------------------
bot_name  | 否    | Str 机器人名
wx_id | 否    | Str 机器人微信号
base64_qrcode | 否    | Str 机器人二维码
create_date | 否    | Str 此机器人信息创建时间 `2017-04-23`
expire_date | 否    | Str 此机器人信息创建时间 `2017-04-23`
remark | 否    | 备注信息
status | 否    | Int 机器人状态码 `-401为已删除`












## 微信群列表管理

### 1\. 新增微信群信息

接口调用请求说明

http请求方式：Post <http://api.xxx.com/api/new_group>


#### 1.1 请求参数说明

加密消息参数  | 是否必须 | 说明
--- | ---- | ---
group_id | 否    | 群ID（重要，用于未来群查找。 可传入，若不传入则自动生成32位随机字符串作为群ID）
group_name | 是    | 群名
group_disc | 是    | 群描述（兴趣描述）
group_catalog1 | 是    | 群分类一级标签 `如 ['编程', '互联网'] 或 ['地区交友', '兴趣']` 
group_catalog2 | 是    | 群分类二级标签 `如 ['Node', '深度学习'] 或 ['大连野营', '户外运动']`
is_admin | 是    | 机器人是否为群主
bot_wx_id | 是    | 提交此信息机器人微信号
code | 是    | 发送给机器人的进群暗号
remark | 否    | 备注信息


返回结果 正确时的返回JSON数据包如下：

```json
{
    "errcode":0,
    "errmsg":"ok",
    "data":[
        {
            "group_id": "DWIADduwaidnIUWDNWdNDWAODWDWMiodwnaod",
            "group_name": "大连户外",
            "group_disc": "喜欢户外运动，大连地区的伙伴们快加入我们吧，不定期举办集体户外活动哦～",
            "group_catalog1": {"地区交友": 31, "兴趣": 94},
            "group_catalog2": {"大连野营": 1, "户外运动": 1},
            "is_admin": "Y",
            "bot_wx_id": "xxxxxx",
            "code": "户外",
            "status": 0
        }
    ]
}
```

错误时的返回JSON数据包如下（示例为机器人ID未找到 `将导致无法提供入群辅助机器人二维码`）：

```json
{
    "errcode":-30203,
    "errmsg":"bot_wx_id not found"
}
```

#### 1.2 data返回参数说明

参数          | 是否必须 | 说明
----------- | ---- | ---------------------
group_id  | 否    | Str 群ID
group_name  | 否    | Str 群名
group_disc | 否    | Str 群描述，一句话介绍
group_catalog1 | 否    | Dict 同类群数量
group_catalog2 | 否    | Dict 在一级分类相同情况下，同类群数量
is_admin | 否    | Str 机器人是否为群主
bot_wx_id | 否    | Str 机器人微信ID
code | 否    | Str 入群暗号
status | 否    | Int 群状态码




### 2\. 微信群停止展示

接口调用请求说明

http请求方式：Post <http://api.xxx.com/api/close_group>


#### 2.1 请求参数说明

加密消息参数  | 是否必须 | 说明
--- | ---- | ---
group_id | 是    | 群ID
remark | 否    | 备注信息


返回结果 正确时的返回JSON数据包如下：

```json
{
    "errcode":0,
    "errmsg":"ok",
    "data":[
        {
            "group_name": "大连户外",
            "group_disc": "喜欢户外运动，大连地区的伙伴们快加入我们吧，不定期举办集体户外活动哦～",
            "bot_wx_id": "xxxxxx",
            "code": "户外",
            "status": -30201
        }
    ]
}
```

错误时的返回JSON数据包如下（示例为group_id未找到）：

```json
{
    "errcode":-30202,
    "errmsg":"group_id not found"
}
```

#### 2.2 data返回参数说明

参数          | 是否必须 | 说明
----------- | ---- | ---------------------
group_name  | 否    | Str 群名
group_disc | 否    | Str 群描述，一句话介绍
bot_wx_id | 否    | Str 机器人微信ID
code | 否    | Str 入群暗号
status | 否    | Int 群状态码


### 3\. 微信群恢复展示

接口调用请求说明

http请求方式：Post <http://api.xxx.com/api/reopen_group>


#### 3.1 请求参数说明

加密消息参数  | 是否必须 | 说明
--- | ---- | ---
group_id | 是    | 群ID
remark | 否    | 备注信息


返回结果 正确时的返回JSON数据包如下：

```json
{
    "errcode":0,
    "errmsg":"ok",
    "data":[
        {
            "group_name": "大连户外",
            "group_disc": "喜欢户外运动，大连地区的伙伴们快加入我们吧，不定期举办集体户外活动哦～",
            "bot_wx_id": "xxxxxx",
            "code": "户外",
            "status": 0
        }
    ]
}
```

错误时的返回JSON数据包如下（示例为当前当前group正常展示状态，无法进行reopen操作）：

```json
{
    "errcode":-30204,
    "errmsg":"group in service"
}
```

#### 3.2 data返回参数说明

参数          | 是否必须 | 说明
----------- | ---- | ---------------------
group_name  | 否    | Str 群名
group_disc | 否    | Str 群描述，一句话介绍
bot_wx_id | 否    | Str 机器人微信ID
code | 否    | Str 入群暗号
status | 否    | Int 群状态码



### 4\. 微信群恢复展示

接口调用请求说明

http请求方式：Post <http://api.xxx.com/api/reopen_group>


#### 4.1 请求参数说明

加密消息参数  | 是否必须 | 说明
--- | ---- | ---
group_id | 是    | 群ID
remark | 否    | 备注信息


返回结果 正确时的返回JSON数据包如下：

```json
{
    "errcode":0,
    "errmsg":"ok",
    "data":[
        {
            "group_name": "大连户外",
            "group_disc": "喜欢户外运动，大连地区的伙伴们快加入我们吧，不定期举办集体户外活动哦～",
            "bot_wx_id": "xxxxxx",
            "code": "户外",
            "status": 0
        }
    ]
}
```

错误时的返回JSON数据包如下（示例为当前当前group正常展示状态，无法进行reopen操作）：

```json
{
    "errcode":-30204,
    "errmsg":"group in service"
}
```

#### 4.2 data返回参数说明

参数          | 是否必须 | 说明
----------- | ---- | ---------------------
group_name  | 否    | Str 群名
group_disc | 否    | Str 群描述，一句话介绍
bot_wx_id | 否    | Str 机器人微信ID
code | 否    | Str 入群暗号
status | 否    | Int 群状态码


### 5\. 微信群信息修改

接口调用请求说明

http请求方式：Post <http://api.xxx.com/api/modify_group>


#### 5.1 请求参数说明

加密消息参数  | 是否必须 | 说明
--- | ---- | ---
group_id | 是    | 群ID
group_name | 否（修改则带此参数）   | 群名
group_disc | 否（修改则带此参数）   | 群描述（兴趣描述）
group_catalog1 | 否（修改则带此参数）  | 群分类一级标签 `如 ['编程', '互联网'] 或 ['地区交友', '兴趣']` 
group_catalog2 | 否（修改则带此参数）  | 群分类二级标签 `如 ['Node', '深度学习'] 或 ['大连野营', '户外运动']`
is_admin | 否（修改则带此参数）  | 机器人是否为群主
bot_wx_id | 否（修改则带此参数）  | 提交此信息机器人微信号
code | 否（修改则带此参数）  | 发送给机器人的进群暗号
remark | 否    | 备注信息


返回结果 正确时的返回JSON数据包如下：

```json
{
    "errcode":0,
    "errmsg":"ok",
    "data":[
        {
            "group_id": "DWIADduwaidnIUWDNWdNDWAODWDWMiodwnaod",
            "group_name": {
                    "new": "大连户外1群",
                    "old": "大连户外"
                },
            "group_disc": {
                    "new": "一起到海边玩吧",
                    "old": "喜欢户外运动，大连地区的伙伴们快加入我们吧，不定期举办集体户外活动哦～"
                },
            "group_catalog1": {
                    "new": "地区交友&兴趣&户外运动",
                    "old": "地区交友&兴趣"
                },
            "group_catalog2": {
                    "new": "大连野营",
                    "old": "大连野营&户外运动"
                },
            "is_admin": {
                    "new": "N",
                    "old": "Y"
                },
            "bot_wx_id": {
                    "new": "xxxxxx01_bot",
                    "old": "xxxxxx"
                },
            "code": {
                    "new": "大连户外",
                    "old": "户外"
                },
            "status": 0
        }
    ]
}
```
错误时的返回JSON数据包如下（示例为当前当前group正常展示状态，无法进行reopen操作）：

```json
{
    "errcode":-30204,
    "errmsg":"group in service"
}
```

#### 5.2 data返回参数说明

参数          | 是否必须 | 说明
----------- | ---- | ---------------------
group_id  | 否    | Str 群ID
group_name  | 否    | Str 群名
group_disc | 否    | Str 群描述，一句话介绍
group_catalog1 | 否    | Str 群一级分类
group_catalog2 | 否    | Str 群二级分类
is_admin | 否    | Str 机器人是否为群主
bot_wx_id | 否    | Str 机器人微信ID
code | 否    | Str 入群暗号
status | 否    | Int 群状态码
