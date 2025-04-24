# 朋友圈模块

在新设备登录后的1-3天内，您将无法使用朋友圈发布、点赞、评论等功能。在此期间，如果尝试进行这些操作，您将收到来自微信团队的提醒。请注意遵守相关规定。

# 点赞/取消点赞

> 在新设备登录后的1-3天内，您将无法使用朋友圈发布、点赞、评论等功能。在此期间，如果尝试进行这些操作，您将收到来自微信团队的提醒。请注意遵守相关规定。

## OpenAPI

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /gewe/v2/api/sns/likeSns:
    post:
      summary: 点赞/取消点赞
      deprecated: false
      description: >-
        在新设备登录后的1-3天内，您将无法使用朋友圈发布、点赞、评论等功能。在此期间，如果尝试进行这些操作，您将收到来自微信团队的提醒。请注意遵守相关规定。
      tags:
        - 基础API/朋友圈模块
      parameters:
        - name: X-GEWE-TOKEN
          in: header
          description: ''
          required: true
          example: '{{gewe-token}}'
          schema:
            type: string
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                appId:
                  type: string
                  description: 设备ID
                  additionalProperties: false
                snsId:
                  type: number
                  description: 朋友圈ID
                operType:
                  type: integer
                  description: 1点赞  2取消点赞
                wxid:
                  type: string
                  description: 点赞的好友wxid
              x-apifox-orders:
                - appId
                - snsId
                - operType
                - wxid
              required:
                - appId
                - snsId
                - operType
                - wxid
            example:
              appId: '{{appid}}'
              snsId: 14287710809635828000
              operType: 2
              wxid: wxid_g66c3f6y1eg922
      responses:
        '200':
          description: ''
          content:
            application/json:
              schema:
                type: object
                properties:
                  ret:
                    type: integer
                  msg:
                    type: string
                required:
                  - ret
                  - msg
                x-apifox-orders:
                  - ret
                  - msg
              example:
                ret: 200
                msg: 操作成功
          headers: {}
          x-apifox-name: 成功
      security: []
      x-apifox-folder: 基础API/朋友圈模块
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3475559/apis/api-139908334-run
components:
  schemas: {}
  securitySchemes: {}
servers:
  - url: http://218.78.116.24:10883
    description: 测试环境
security: []

```

# 删除朋友圈

## OpenAPI

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /gewe/v2/api/sns/delSns:
    post:
      summary: 删除朋友圈
      deprecated: false
      description: ''
      tags:
        - 基础API/朋友圈模块
      parameters:
        - name: X-GEWE-TOKEN
          in: header
          description: ''
          required: true
          example: '{{gewe-token}}'
          schema:
            type: string
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                appId:
                  type: string
                  description: 设备ID
                  additionalProperties: false
                  nullable: true
                snsId:
                  type: number
                  description: 朋友圈ID
                  nullable: true
              x-apifox-orders:
                - appId
                - snsId
              required:
                - appId
                - snsId
            example:
              appId: '{{appid}}'
              snsId: 14292805691027100000
      responses:
        '200':
          description: ''
          content:
            application/json:
              schema:
                type: object
                properties:
                  ret:
                    type: integer
                  msg:
                    type: string
                required:
                  - ret
                  - msg
                x-apifox-orders:
                  - ret
                  - msg
              example:
                ret: 200
                msg: 操作成功
          headers: {}
          x-apifox-name: 成功
      security: []
      x-apifox-folder: 基础API/朋友圈模块
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3475559/apis/api-139908335-run
components:
  schemas: {}
  securitySchemes: {}
servers:
  - url: http://218.78.116.24:10883
    description: 测试环境
security: []

```

# 设置朋友圈可见范围

> #### 朋友圈可见范围 option 可选项
- 1:全部
- 2:最近半年
- 3:最近一个月
- 4:最近三天

## OpenAPI

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /gewe/v2/api/sns/snsVisibleScope:
    post:
      summary: 设置朋友圈可见范围
      deprecated: false
      description: |-
        #### 朋友圈可见范围 option 可选项
        - 1:全部
        - 2:最近半年
        - 3:最近一个月
        - 4:最近三天
      tags:
        - 基础API/朋友圈模块
      parameters:
        - name: X-GEWE-TOKEN
          in: header
          description: ''
          required: true
          example: '{{gewe-token}}'
          schema:
            type: string
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                appId:
                  type: string
                  description: 设备ID
                  additionalProperties: false
                option:
                  type: number
                  description: 朋友圈可见范围
              x-apifox-orders:
                - appId
                - option
              required:
                - appId
                - option
            example:
              appId: '{{appid}}'
              option: 3
      responses:
        '200':
          description: ''
          content:
            application/json:
              schema:
                type: object
                properties:
                  ret:
                    type: integer
                  msg:
                    type: string
                required:
                  - ret
                  - msg
                x-apifox-orders:
                  - ret
                  - msg
              example:
                ret: 200
                msg: 操作成功
          headers: {}
          x-apifox-name: 成功
      security: []
      x-apifox-folder: 基础API/朋友圈模块
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3475559/apis/api-139908336-run
components:
  schemas: {}
  securitySchemes: {}
servers:
  - url: http://218.78.116.24:10883
    description: 测试环境
security: []

```

# 是否允许陌生人查看朋友圈

## OpenAPI

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /gewe/v2/api/sns/strangerVisibilityEnabled:
    post:
      summary: 是否允许陌生人查看朋友圈
      deprecated: false
      description: ''
      tags:
        - 基础API/朋友圈模块
      parameters:
        - name: X-GEWE-TOKEN
          in: header
          description: ''
          required: true
          example: '{{gewe-token}}'
          schema:
            type: string
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                appId:
                  type: string
                  description: 设备ID
                  additionalProperties: false
                enabled:
                  type: boolean
                  description: 是否允许
              x-apifox-orders:
                - appId
                - enabled
              required:
                - appId
                - enabled
            example:
              appId: '{{appid}}'
              enabled: true
      responses:
        '200':
          description: ''
          content:
            application/json:
              schema:
                type: object
                properties:
                  ret:
                    type: integer
                  msg:
                    type: string
                required:
                  - ret
                  - msg
                x-apifox-orders:
                  - ret
                  - msg
              example:
                ret: 200
                msg: 操作成功
          headers: {}
          x-apifox-name: 成功
      security: []
      x-apifox-folder: 基础API/朋友圈模块
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3475559/apis/api-139908337-run
components:
  schemas: {}
  securitySchemes: {}
servers:
  - url: http://218.78.116.24:10883
    description: 测试环境
security: []

```

# 设置某条朋友圈为隐私/公开

## OpenAPI

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /gewe/v2/api/sns/snsSetPrivacy:
    post:
      summary: 设置某条朋友圈为隐私/公开
      deprecated: false
      description: ''
      tags:
        - 基础API/朋友圈模块
      parameters:
        - name: X-GEWE-TOKEN
          in: header
          description: ''
          required: true
          example: '{{gewe-token}}'
          schema:
            type: string
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                appId:
                  type: string
                  description: 设备ID
                  additionalProperties: false
                snsId:
                  type: number
                  description: 朋友圈ID
                open:
                  type: boolean
                  description: 是否公开
              x-apifox-orders:
                - appId
                - snsId
                - open
              required:
                - appId
                - snsId
                - open
            example:
              appId: '{{appid}}'
              snsId: 14214000407987818000
              open: true
      responses:
        '200':
          description: ''
          content:
            application/json:
              schema:
                type: object
                properties:
                  ret:
                    type: integer
                  msg:
                    type: string
                required:
                  - ret
                  - msg
                x-apifox-orders:
                  - ret
                  - msg
              example:
                ret: 200
                msg: 操作成功
          headers: {}
          x-apifox-name: 成功
      security: []
      x-apifox-folder: 基础API/朋友圈模块
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3475559/apis/api-139908338-run
components:
  schemas: {}
  securitySchemes: {}
servers:
  - url: http://218.78.116.24:10883
    description: 测试环境
security: []

```

# 下载朋友圈视频

## OpenAPI

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /gewe/v2/api/sns/downloadSnsVideo:
    post:
      summary: 下载朋友圈视频
      deprecated: false
      description: ''
      tags:
        - 基础API/朋友圈模块
      parameters:
        - name: X-GEWE-TOKEN
          in: header
          description: ''
          required: true
          example: '{{gewe-token}}'
          schema:
            type: string
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                appId:
                  type: string
                  description: 设备ID
                  additionalProperties: false
                snsXml:
                  type: string
                  description: 获取到的朋友圈xml
              x-apifox-orders:
                - appId
                - snsXml
              required:
                - appId
                - snsXml
            example:
              appId: '{{appid}}'
              snsXml: >-
                <TimelineObject><id>14362242802440999552</id><username>wxid_8zbdraznmhf622</username><createTime>1712112760</createTime><contentDesc>hhhh</contentDesc><contentDescShowType>0</contentDescShowType><contentDescScene>0</contentDescScene><private>0</private><sightFolded>0</sightFolded><showFlag>0</showFlag><appInfo><id></id><version></version><appName></appName><installUrl></installUrl><fromUrl></fromUrl><isForceUpdate>0</isForceUpdate><isHidden>0</isHidden></appInfo><sourceUserName></sourceUserName><sourceNickName></sourceNickName><statisticsData></statisticsData><statExtStr></statExtStr><ContentObject><contentStyle>15</contentStyle><title>微信小视频</title><description>Sight</description><mediaList><media><enc
                key="2997485059">1</enc><id>14362242803293950611</id><type>6</type><title></title><description>hhhh</description><private>0</private><userData></userData><subType>0</subType><videoSize
                width="720" height="1280"></videoSize><url type="1"
                md5="e91f4a52d34e4c1334e8c99636f2821b"
                videomd5="7d7876b15379694899f8a6b5ea0273ec">http://shzjwxsns.video.qq.com/102/20202/snsvideodownload?encfilekey=WTva9YVXqXcSUicrMCercmGqzPeuNbNeeu9ZqrbBsnKm0QmEwmBELXy9Yrnibdria8Uyz1UwdCpyXhqvwiaRAxVHLuB0rcTBp6zEhUc2ZHD9HjEcPw68CpgMjav3TdXFMnR9SBTFOsiahMDo&amp;token=AxricY7RBHdWLnyNFyR4AOwrBQ2416HD0BiaYaicRHia1AANLTz79sUIJMDhgibIrd1yVicmsQoyth8gE&amp;idx=1&amp;bizid=1023&amp;dotrans=1&amp;dur=10&amp;ef=0_0&amp;hy=SH&amp;ilogo=2&amp;upid=500130</url><thumb
                type="1">http://vweixinthumb.tc.qq.com/150/20250/snsvideodownload?encfilekey=WTva9YVXqXcSUicrMCercmBpUQNWanXicGFgrN3zItA0icXh48zcxffrFua0M7vPyibE6ZG0FFBwDB7ong1JpPTLNC89ZcyJVJsG7ZYibpo0hXu8Us6PQXBUIWelFZKUFEexAgZWxia5ib6ibvM&amp;token=AxricY7RBHdWLnyNFyR4AOwrBQ2416HD0BiaYaicRHia1AAic3UNt8mjEQHdgfv6Iw06R0sBB36LFDhk&amp;idx=1&amp;bizid=1023&amp;hy=SH</thumb><size
                width="224.000000" height="398.000000"
                totalSize="458568"></size><videoDuration>10.434000</videoDuration><VideoColdDLRule><All>CAISBAgWEAEoAjAc</All></VideoColdDLRule></media></mediaList><contentUrl>https://support.weixin.qq.com/cgi-bin/mmsupport-bin/readtemplate?t=page/common_page__upgrade&amp;v=1</contentUrl></ContentObject><actionInfo><appMsg><messageAction></messageAction></appMsg></actionInfo><location
                poiClassifyId="" poiName="" poiAddress="" poiClassifyType="0"
                city=""></location><publicUserName></publicUserName><streamvideo><streamvideourl></streamvideourl><streamvideothumburl></streamvideothumburl><streamvideoweburl></streamvideoweburl></streamvideo></TimelineObject>
      responses:
        '200':
          description: ''
          content:
            application/json:
              schema:
                type: object
                properties:
                  ret:
                    type: integer
                  msg:
                    type: string
                  data:
                    type: object
                    properties:
                      fileUrl:
                        type: string
                    required:
                      - fileUrl
                    x-apifox-orders:
                      - fileUrl
                required:
                  - ret
                  - msg
                  - data
                x-apifox-orders:
                  - ret
                  - msg
                  - data
              example:
                ret: 200
                msg: 操作成功
                data:
                  fileUrl: >-
                    http://oos-sccd.ctyunapi.cn/20240403/wx_sP8zmJIXLkWupGnKoF/04847c12-cf2a-4850-9b8e-2d3b40190aaa.mp4?AWSAccessKeyId=9e882e7187c38b431303&Expires=1712720598&Signature=i2%2FwckXedEf%2BYvg1Az%2FHJ2VWL9E%3D
          headers: {}
          x-apifox-name: 成功
      security: []
      x-apifox-folder: 基础API/朋友圈模块
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3475559/apis/api-139908339-run
components:
  schemas: {}
  securitySchemes: {}
servers:
  - url: http://218.78.116.24:10883
    description: 测试环境
security: []

```

# 发送文字朋友圈

> 在新设备登录后的1-3天内，您将无法使用朋友圈发布、点赞、评论等功能。在此期间，如果尝试进行这些操作，您将收到来自微信团队的提醒。请注意遵守相关规定。

## OpenAPI

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /gewe/v2/api/sns/sendTextSns:
    post:
      summary: 发送文字朋友圈
      deprecated: false
      description: >-
        在新设备登录后的1-3天内，您将无法使用朋友圈发布、点赞、评论等功能。在此期间，如果尝试进行这些操作，您将收到来自微信团队的提醒。请注意遵守相关规定。
      tags:
        - 基础API/朋友圈模块
      parameters:
        - name: X-GEWE-TOKEN
          in: header
          description: ''
          required: true
          example: '{{gewe-token}}'
          schema:
            type: string
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                appId:
                  type: string
                  description: 设备ID
                  additionalProperties: false
                allowWxIds:
                  type: array
                  items:
                    type: string
                    description: 好友的wxid
                  description: 允许谁看
                atWxIds:
                  type: array
                  items:
                    type: string
                    description: 好友的wxid
                  description: 提醒谁看
                disableWxIds:
                  type: array
                  items:
                    type: string
                    description: 好友的wxid
                  description: 不给谁看
                privacy:
                  type: boolean
                  description: 是否私密
                  default: 'false'
                content:
                  type: string
                  description: 朋友圈文字内容
                allowTagIds:
                  type: array
                  items:
                    type: string
                    description: 标签id
                  description: 允许谁看（标签id）
                disableTagIds:
                  type: array
                  items:
                    type: string
                    description: 标签id
                  description: 不给谁看（标签id）
              x-apifox-orders:
                - appId
                - allowWxIds
                - atWxIds
                - disableWxIds
                - privacy
                - content
                - allowTagIds
                - disableTagIds
              required:
                - appId
                - content
            example:
              appId: '{{appid}}'
              allowWxIds: []
              atWxIds: []
              disableWxIds: []
              content: test
              privacy: false
              allowTagIds: []
              disableTagIds: []
      responses:
        '200':
          description: ''
          content:
            application/json:
              schema:
                type: object
                properties:
                  ret:
                    type: integer
                  msg:
                    type: string
                  data:
                    type: object
                    properties:
                      id:
                        type: integer
                        description: 朋友圈ID
                      userName:
                        type: string
                        description: 朋友圈作者的wxid
                      nickName:
                        type: string
                        description: 朋友圈作者的昵称
                      createTime:
                        type: integer
                        description: 发布时间
                    required:
                      - id
                      - userName
                      - nickName
                      - createTime
                    x-apifox-orders:
                      - id
                      - userName
                      - nickName
                      - createTime
                required:
                  - ret
                  - msg
                  - data
                x-apifox-orders:
                  - ret
                  - msg
                  - data
              example:
                ret: 200
                msg: 操作成功
                data:
                  id: 14287800629617234000
                  userName: zhangchuan2288
                  nickName: 朝夕。
                  createTime: 1703238562
          headers: {}
          x-apifox-name: 成功
      security: []
      x-apifox-folder: 基础API/朋友圈模块
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3475559/apis/api-139908340-run
components:
  schemas: {}
  securitySchemes: {}
servers:
  - url: http://218.78.116.24:10883
    description: 测试环境
security: []

```


# 发送图片朋友圈

> 在新设备登录后的1-3天内，您将无法使用朋友圈发布、点赞、评论等功能。在此期间，如果尝试进行这些操作，您将收到来自微信团队的提醒。请注意遵守相关规定。

#### 注意
本接口的imgInfos参数需通过 [上传朋友圈图片接口](http://doc.geweapi.com/api-139908344) 获取

## OpenAPI

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /gewe/v2/api/sns/sendImgSns:
    post:
      summary: 发送图片朋友圈
      deprecated: false
      description: >-
        在新设备登录后的1-3天内，您将无法使用朋友圈发布、点赞、评论等功能。在此期间，如果尝试进行这些操作，您将收到来自微信团队的提醒。请注意遵守相关规定。


        #### 注意

        本接口的imgInfos参数需通过 [上传朋友圈图片接口](http://doc.geweapi.com/api-139908344) 获取
      tags:
        - 基础API/朋友圈模块
      parameters:
        - name: X-GEWE-TOKEN
          in: header
          description: ''
          required: true
          example: '{{gewe-token}}'
          schema:
            type: string
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                appId:
                  type: string
                  description: 设备ID
                  additionalProperties: false
                allowWxIds:
                  type: array
                  items:
                    type: string
                    description: 好友的wxid
                  description: 允许谁看
                atWxIds:
                  type: array
                  items:
                    type: string
                    description: 好友的wxid
                  description: 提醒谁看
                disableWxIds:
                  type: array
                  items:
                    type: string
                    description: 好友的wxid
                  description: 不给谁看
                privacy:
                  type: boolean
                  description: 是否私密
                  default: 'false'
                content:
                  type: string
                  description: 朋友圈文字内容
                imgInfos:
                  type: array
                  items:
                    type: object
                    properties:
                      fileUrl:
                        type: string
                      thumbUrl:
                        type: string
                      fileMd5:
                        type: string
                      length:
                        type: number
                      width:
                        type: number
                        description: 图片宽度
                      height:
                        type: number
                        description: 图片高度
                    x-apifox-orders:
                      - fileUrl
                      - thumbUrl
                      - fileMd5
                      - length
                      - width
                      - height
                    required:
                      - fileUrl
                      - thumbUrl
                      - fileMd5
                      - width
                      - height
                  description: 通过上传朋友圈图片接口获取
                  minItems: 1
                  maxItems: 9
                allowTagIds:
                  type: array
                  items:
                    type: string
                    description: 标签id
                  description: 允许谁看（标签id）
                disableTagIds:
                  type: array
                  items:
                    type: string
                    description: 标签id
                  description: 不给谁看（标签id）
              x-apifox-orders:
                - appId
                - allowWxIds
                - atWxIds
                - disableWxIds
                - privacy
                - content
                - imgInfos
                - allowTagIds
                - disableTagIds
              required:
                - appId
                - imgInfos
            example:
              appId: '{{appid}}'
              allowWxIds: []
              atWxIds: []
              disableWxIds: []
              content: img
              imgInfos:
                - fileUrl: >-
                    http://szmmsns.qpic.cn/mmsns/FzeKA69P5uJr4JZ7M7h6bAeMo2q3AKbyA2aqtKtBTibicSJdhlBuc30AMOCFkCYdnCxleUX35NBBE/0
                  thumbUrl: >-
                    http://szmmsns.qpic.cn/mmsns/FzeKA69P5uJr4JZ7M7h6bAeMo2q3AKbyA2aqtKtBTibicSJdhlBuc30AMOCFkCYdnCxleUX35NBBE/150
                  fileMd5: 704de7ebbc107a51a4f0986253a6d3b6
                  length: 1096
                  width: 1920
                  height: 1080
                - fileUrl: >-
                    http://szmmsns.qpic.cn/mmsns/FzeKA69P5uJr4JZ7M7h6bAeMo2q3AKby5mg2I3C20yLn95mWHQ0dC4hqWosWyf1zf43Xmut3CCE/0
                  thumbUrl: >-
                    http://szmmsns.qpic.cn/mmsns/FzeKA69P5uJr4JZ7M7h6bAeMo2q3AKby5mg2I3C20yLn95mWHQ0dC4hqWosWyf1zf43Xmut3CCE/150
                  fileMd5: f34ccc016a83c23d11b94f9c4ef533f3
                  length: 1086
                  width: 1920
                  height: 1080
              privacy: false
              allowTagIds: []
              disableTagIds: []
      responses:
        '200':
          description: ''
          content:
            application/json:
              schema:
                type: object
                properties:
                  ret:
                    type: integer
                  msg:
                    type: string
                  data:
                    type: object
                    properties:
                      id:
                        type: integer
                        description: 朋友圈ID
                      userName:
                        type: string
                        description: 朋友圈作者的wxid
                      nickName:
                        type: string
                        description: 朋友圈作者的昵称
                      createTime:
                        type: integer
                        description: 发布时间
                    required:
                      - id
                      - userName
                      - nickName
                      - createTime
                    x-apifox-orders:
                      - id
                      - userName
                      - nickName
                      - createTime
                required:
                  - ret
                  - msg
                  - data
                x-apifox-orders:
                  - ret
                  - msg
                  - data
              example:
                ret: 200
                msg: 操作成功
                data:
                  id: 14292802719912825000
                  userName: zhangchuan2288
                  nickName: 朝夕。
                  createTime: 1703834858
          headers: {}
          x-apifox-name: 成功
      security: []
      x-apifox-folder: 基础API/朋友圈模块
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3475559/apis/api-139908341-run
components:
  schemas: {}
  securitySchemes: {}
servers:
  - url: http://218.78.116.24:10883
    description: 测试环境
security: []

```

# 发送视频朋友圈

> 在新设备登录后的1-3天内，您将无法使用朋友圈发布、点赞、评论等功能。在此期间，如果尝试进行这些操作，您将收到来自微信团队的提醒。请注意遵守相关规定。

#### 注意
本接口的videoInfo参数需通过 [上传朋友圈视频接口](http://doc.geweapi.com/api-139908345) 获取

## OpenAPI

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /gewe/v2/api/sns/sendVideoSns:
    post:
      summary: 发送视频朋友圈
      deprecated: false
      description: >-
        在新设备登录后的1-3天内，您将无法使用朋友圈发布、点赞、评论等功能。在此期间，如果尝试进行这些操作，您将收到来自微信团队的提醒。请注意遵守相关规定。


        #### 注意

        本接口的videoInfo参数需通过 [上传朋友圈视频接口](http://doc.geweapi.com/api-139908345) 获取
      tags:
        - 基础API/朋友圈模块
      parameters:
        - name: X-GEWE-TOKEN
          in: header
          description: ''
          required: true
          example: '{{gewe-token}}'
          schema:
            type: string
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                appId:
                  type: string
                  description: 设备ID
                  additionalProperties: false
                allowWxIds:
                  type: array
                  items:
                    type: string
                    description: 好友的wxid
                  description: 允许谁看
                atWxIds:
                  type: array
                  items:
                    type: string
                    description: 好友的wxid
                  description: 提醒谁看
                disableWxIds:
                  type: array
                  items:
                    type: string
                    description: 好友的wxid
                  description: 不给谁看
                privacy:
                  type: boolean
                  description: 是否私密
                  default: 'false'
                content:
                  type: string
                  description: 朋友圈文字内容
                videoInfo:
                  type: object
                  properties:
                    fileUrl:
                      type: string
                    thumbUrl:
                      type: string
                    fileMd5:
                      type: string
                    length:
                      type: number
                  x-apifox-orders:
                    - fileUrl
                    - thumbUrl
                    - fileMd5
                    - length
                  required:
                    - fileUrl
                    - fileMd5
                    - thumbUrl
                  description: 通过上传朋友圈视频接口获取
                allowTagIds:
                  type: array
                  items:
                    type: string
                    description: 标签id
                  description: 允许谁看（标签id）
                disableTagIds:
                  type: array
                  items:
                    type: string
                    description: 标签id
                  description: 不给谁看（标签id）
              x-apifox-orders:
                - appId
                - allowWxIds
                - atWxIds
                - disableWxIds
                - privacy
                - content
                - videoInfo
                - allowTagIds
                - disableTagIds
              required:
                - appId
                - videoInfo
            example:
              appId: '{{appid}}'
              allowWxIds: []
              atWxIds: []
              disableWxIds: []
              content: in
              videoInfo:
                fileUrl: >-
                  http://szzjwxsns.video.qq.com/102/20202/snsvideodownload?filekey=30340201010420301e0201660402535a04106e95f9d79588843ac259b780f0cbf20f020314148b040d00000004627466730000000132&hy=SZ&storeid=5658e7541000080a98399cc840000006600004eea535a236b0181565ff0c9a&dotrans=9&ef=30_0&ut=6xykWLEnztInqJIccsNnmJnFIIMYTDicqsNxakAGmcmW1hOicyiayN6Cw&ui=1&bizid=1023&ilogo=2&dur=7&upid=500030
                thumbUrl: >-
                  http://vweixinthumb.tc.qq.com/150/20250/snsvideodownload?filekey=30340201010420301e020200960402535a0410704de7ebbc107a51a4f0986253a6d3b602020448040d00000004627466730000000132&hy=SZ&storeid=5658e7541000065838399cc840000009600004f1a535a236cc15156605b59d&bizid=1023
                fileMd5: 6e95f9d79588843ac259b780f0cbf20f
                length: 1315979
              privacy: false
              allowTagIds: []
              disableTagIds: []
      responses:
        '200':
          description: ''
          content:
            application/json:
              schema:
                type: object
                properties:
                  ret:
                    type: integer
                  msg:
                    type: string
                  data:
                    type: object
                    properties:
                      id:
                        type: integer
                        description: 朋友圈ID
                      userName:
                        type: string
                        description: 朋友圈作者的wxid
                      nickName:
                        type: string
                        description: 朋友圈作者的昵称
                      createTime:
                        type: integer
                        description: 发布时间
                    required:
                      - id
                      - userName
                      - nickName
                      - createTime
                    x-apifox-orders:
                      - id
                      - userName
                      - nickName
                      - createTime
                required:
                  - ret
                  - msg
                  - data
                x-apifox-orders:
                  - ret
                  - msg
                  - data
              example:
                ret: 200
                msg: 操作成功
                data:
                  id: 14292804021433274000
                  userName: zhangchuan2288
                  nickName: 朝夕。
                  createTime: 1703835013
          headers: {}
          x-apifox-name: 成功
      security: []
      x-apifox-folder: 基础API/朋友圈模块
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3475559/apis/api-139908342-run
components:
  schemas: {}
  securitySchemes: {}
servers:
  - url: http://218.78.116.24:10883
    description: 测试环境
security: []

```

# 发送链接朋友圈

> 在新设备登录后的1-3天内，您将无法使用朋友圈发布、点赞、评论等功能。在此期间，如果尝试进行这些操作，您将收到来自微信团队的提醒。请注意遵守相关规定。

## OpenAPI

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /gewe/v2/api/sns/sendUrlSns:
    post:
      summary: 发送链接朋友圈
      deprecated: false
      description: >-
        在新设备登录后的1-3天内，您将无法使用朋友圈发布、点赞、评论等功能。在此期间，如果尝试进行这些操作，您将收到来自微信团队的提醒。请注意遵守相关规定。
      tags:
        - 基础API/朋友圈模块
      parameters:
        - name: X-GEWE-TOKEN
          in: header
          description: ''
          required: true
          example: '{{gewe-token}}'
          schema:
            type: string
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                appId:
                  type: string
                  description: 设备ID
                  additionalProperties: false
                allowWxIds:
                  type: array
                  items:
                    type: string
                    description: 好友的wxid
                  description: 允许谁看
                atWxIds:
                  type: array
                  items:
                    type: string
                    description: 好友的wxid
                  description: 提醒谁看
                disableWxIds:
                  type: array
                  items:
                    type: string
                    description: 好友的wxid
                  description: 不给谁看
                privacy:
                  type: boolean
                  description: 是否私密
                  default: 'false'
                content:
                  type: string
                  description: 朋友圈文字内容
                thumbUrl:
                  type: string
                  description: 链接缩略图
                linkUrl:
                  type: string
                  description: 链接地址
                title:
                  type: string
                  description: 链接标题
                description:
                  type: string
                  description: 链接描述
                allowTagIds:
                  type: array
                  items:
                    type: string
                    description: 标签id
                  description: 允许谁看（标签id）
                disableTagIds:
                  type: array
                  items:
                    type: string
                    description: 标签id
                  description: 不给谁看（标签id）
              x-apifox-orders:
                - appId
                - allowWxIds
                - atWxIds
                - disableWxIds
                - privacy
                - content
                - thumbUrl
                - linkUrl
                - title
                - description
                - allowTagIds
                - disableTagIds
              required:
                - appId
                - description
                - title
                - linkUrl
                - thumbUrl
            example:
              appId: '{{appid}}'
              allowWxIds: []
              atWxIds: []
              disableWxIds: []
              content: fugiat sint
              description: >-
                少建片规维门部好将门身对教实们十。一样八七太度及装电部力议应象好。标备北每备志活向较战同光体他。书从线复几细决并面很值话以上。做地江同般劳百山易率干当育起。把件市政层往响包况队算制发。
              title: 族片物
              linkUrl: >-
                https://mbd.baidu.com/newspage/data/landingsuper?context=%7B%22nid%22%3A%22news_9648993262816279801%22%7D&n_type=-1&p_from=-1
              thumbUrl: >-
                https://pics7.baidu.com/feed/a1ec08fa513d269708aaf6569302e2f64216d843.jpeg@f_auto?token=6e5f324904b76e282b92e6c480b80cda
              privacy: false
              allowTagIds: []
              disableTagIds: []
      responses:
        '200':
          description: ''
          content:
            application/json:
              schema:
                type: object
                properties:
                  ret:
                    type: integer
                  msg:
                    type: string
                  data:
                    type: object
                    properties:
                      id:
                        type: integer
                        description: 朋友圈ID
                      userName:
                        type: string
                        description: 朋友圈作者的wxid
                      nickName:
                        type: string
                        description: 朋友圈作者的昵称
                      createTime:
                        type: integer
                        description: 发布时间
                    required:
                      - id
                      - userName
                      - nickName
                      - createTime
                    x-apifox-orders:
                      - id
                      - userName
                      - nickName
                      - createTime
                required:
                  - ret
                  - msg
                  - data
                x-apifox-orders:
                  - ret
                  - msg
                  - data
              example:
                ret: 200
                msg: 操作成功
                data:
                  id: 14292804688606990000
                  userName: zhangchuan2288
                  nickName: 朝夕。
                  createTime: 1703835092
          headers: {}
          x-apifox-name: 成功
      security: []
      x-apifox-folder: 基础API/朋友圈模块
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3475559/apis/api-139908343-run
components:
  schemas: {}
  securitySchemes: {}
servers:
  - url: http://218.78.116.24:10883
    description: 测试环境
security: []

```

# 上传朋友圈图片

## OpenAPI

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /gewe/v2/api/sns/uploadSnsImage:
    post:
      summary: 上传朋友圈图片
      deprecated: false
      description: ''
      tags:
        - 基础API/朋友圈模块
      parameters:
        - name: X-GEWE-TOKEN
          in: header
          description: ''
          required: true
          example: '{{gewe-token}}'
          schema:
            type: string
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                appId:
                  type: string
                  description: 设备ID
                  additionalProperties: false
                imgUrls:
                  type: array
                  items:
                    type: string
                    description: 图片链接
                    minLength: 1
                    maxLength: 9
                  description: 图片链接
              x-apifox-orders:
                - appId
                - imgUrls
              required:
                - appId
                - imgUrls
            example:
              appId: '{{appid}}'
              imgUrls:
                - http://dummyimage.com/400x400
                - http://dummyimage.com/400x300
                - http://dummyimage.com/400x400
                - http://dummyimage.com/400x300
                - http://dummyimage.com/400x400
                - http://dummyimage.com/400x300
                - http://dummyimage.com/400x400
                - http://dummyimage.com/400x300
                - http://dummyimage.com/400x300
                - http://dummyimage.com/400x300
      responses:
        '200':
          description: ''
          content:
            application/json:
              schema:
                type: object
                properties:
                  ret:
                    type: integer
                  msg:
                    type: string
                  data:
                    type: array
                    items:
                      type: object
                      properties:
                        fileUrl:
                          type: string
                          description: 上传图片的链接
                        thumbUrl:
                          type: string
                          description: 上传图片的缩略图链接
                        fileMd5:
                          type: string
                          description: 图片的md5
                        length:
                          type: integer
                          description: 图片的文件大小
                        width:
                          type: integer
                          description: 图片宽度
                        height:
                          type: integer
                          description: 图片高度
                      required:
                        - fileUrl
                        - thumbUrl
                        - fileMd5
                        - length
                        - width
                        - height
                      x-apifox-orders:
                        - fileUrl
                        - thumbUrl
                        - fileMd5
                        - length
                        - width
                        - height
                required:
                  - ret
                  - msg
                  - data
                x-apifox-orders:
                  - ret
                  - msg
                  - data
              examples:
                '1':
                  summary: 成功示例
                  value:
                    ret: 200
                    msg: 操作成功
                    data:
                      - fileUrl: >-
                          http://szmmsns.qpic.cn/mmsns/FzeKA69P5uJr4JZ7M7h6bAeMo2q3AKbyA2aqtKtBTibicSJdhlBuc30AMOCFkCYdnCxleUX35NBBE/0
                        thumbUrl: >-
                          http://szmmsns.qpic.cn/mmsns/FzeKA69P5uJr4JZ7M7h6bAeMo2q3AKbyA2aqtKtBTibicSJdhlBuc30AMOCFkCYdnCxleUX35NBBE/150
                        fileMd5: 704de7ebbc107a51a4f0986253a6d3b6
                        length: 1096
                        width: 1920
                        height: 1080
                      - fileUrl: >-
                          http://szmmsns.qpic.cn/mmsns/FzeKA69P5uJr4JZ7M7h6bAeMo2q3AKby5mg2I3C20yLn95mWHQ0dC4hqWosWyf1zf43Xmut3CCE/0
                        thumbUrl: >-
                          http://szmmsns.qpic.cn/mmsns/FzeKA69P5uJr4JZ7M7h6bAeMo2q3AKby5mg2I3C20yLn95mWHQ0dC4hqWosWyf1zf43Xmut3CCE/150
                        fileMd5: f34ccc016a83c23d11b94f9c4ef533f3
                        length: 1086
                        width: 1920
                        height: 1080
                '2':
                  summary: 异常示例
                  value:
                    ret: 500
                    msg: imgUrls不可为空
          headers: {}
          x-apifox-name: 成功
      security: []
      x-apifox-folder: 基础API/朋友圈模块
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3475559/apis/api-139908344-run
components:
  schemas: {}
  securitySchemes: {}
servers:
  - url: http://218.78.116.24:10883
    description: 测试环境
security: []

```

# 上传朋友圈视频

## OpenAPI

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /gewe/v2/api/sns/uploadSnsVideo:
    post:
      summary: 上传朋友圈视频
      deprecated: false
      description: ''
      tags:
        - 基础API/朋友圈模块
      parameters:
        - name: X-GEWE-TOKEN
          in: header
          description: ''
          required: true
          example: '{{gewe-token}}'
          schema:
            type: string
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                appId:
                  type: string
                  description: 设备ID
                  additionalProperties: false
                  nullable: true
                thumbUrl:
                  type: string
                  description: 视频封面图片链接
                  nullable: true
                videoUrl:
                  type: string
                  description: 视频文件链接
                  nullable: true
              x-apifox-orders:
                - appId
                - thumbUrl
                - videoUrl
              required:
                - appId
                - thumbUrl
                - videoUrl
            example:
              appId: '{{appid}}'
              thumbUrl: http://dummyimage.com/400x400
              videoUrl: >-
                https://scrm-1308498490.cos.ap-shanghai.myqcloud.com/pkg/436fa030-18a45a6e917.mp4?q-sign-algorithm=sha1&q-ak=AKIDmOkqfDUUDfqjMincBSSAbleGaeQv96mB&q-sign-time=1703834932;1703842132&q-key-time=1703834932;1703842132&q-header-list=&q-url-param-list=&q-signature=985cb175fc372408498498294f5c8ddf13a13cfb
      responses:
        '200':
          description: ''
          content:
            application/json:
              schema:
                type: object
                properties:
                  ret:
                    type: integer
                  msg:
                    type: string
                  data:
                    type: object
                    properties:
                      fileUrl:
                        type: string
                        description: 上传视频的文件链接
                      thumbUrl:
                        type: string
                        description: 上传视频的缩略图链接
                      fileMd5:
                        type: string
                        description: 视频的md5
                      length:
                        type: integer
                        description: 视频文件的大小
                    required:
                      - fileUrl
                      - thumbUrl
                      - fileMd5
                      - length
                    x-apifox-orders:
                      - fileUrl
                      - thumbUrl
                      - fileMd5
                      - length
                required:
                  - ret
                  - msg
                  - data
                x-apifox-orders:
                  - ret
                  - msg
                  - data
              example:
                ret: 200
                msg: 操作成功
                data:
                  fileUrl: >-
                    http://szzjwxsns.video.qq.com/102/20202/snsvideodownload?filekey=30340201010420301e0201660402535a04106e95f9d79588843ac259b780f0cbf20f020314148b040d00000004627466730000000132&hy=SZ&storeid=5658e7541000080a98399cc840000006600004eea535a236b0181565ff0c9a&dotrans=9&ef=30_0&ut=6xykWLEnztInqJIccsNnmJnFIIMYTDicqsNxakAGmcmW1hOicyiayN6Cw&ui=1&bizid=1023&ilogo=2&dur=7&upid=500030
                  thumbUrl: >-
                    http://vweixinthumb.tc.qq.com/150/20250/snsvideodownload?filekey=30340201010420301e020200960402535a0410704de7ebbc107a51a4f0986253a6d3b602020448040d00000004627466730000000132&hy=SZ&storeid=5658e7541000065838399cc840000009600004f1a535a236cc15156605b59d&bizid=1023
                  fileMd5: 6e95f9d79588843ac259b780f0cbf20f
                  length: 1315979
          headers: {}
          x-apifox-name: 成功
      security: []
      x-apifox-folder: 基础API/朋友圈模块
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3475559/apis/api-139908345-run
components:
  schemas: {}
  securitySchemes: {}
servers:
  - url: http://218.78.116.24:10883
    description: 测试环境
security: []

```

# 转发朋友圈

> 在新设备登录后的1-3天内，您将无法使用朋友圈发布、点赞、评论等功能。在此期间，如果尝试进行这些操作，您将收到来自微信团队的提醒。请注意遵守相关规定。


## OpenAPI

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /gewe/v2/api/sns/forwardSns:
    post:
      summary: 转发朋友圈
      deprecated: false
      description: >
        在新设备登录后的1-3天内，您将无法使用朋友圈发布、点赞、评论等功能。在此期间，如果尝试进行这些操作，您将收到来自微信团队的提醒。请注意遵守相关规定。
      tags:
        - 基础API/朋友圈模块
      parameters:
        - name: X-GEWE-TOKEN
          in: header
          description: ''
          required: true
          example: '{{gewe-token}}'
          schema:
            type: string
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                appId:
                  type: string
                  description: 设备ID
                  additionalProperties: false
                  nullable: true
                allowWxIds:
                  type: array
                  items:
                    type: string
                    description: 好友的wxid
                  description: 允许谁看
                atWxIds:
                  type: array
                  items:
                    type: string
                    description: 好友的wxid
                  description: 提醒谁看
                disableWxIds:
                  type: array
                  items:
                    type: string
                    description: 好友的wxid
                  description: 不给谁看
                privacy:
                  type: boolean
                  description: 是否私密
                  default: 'false'
                  nullable: true
                snsXml:
                  type: string
                  description: 朋友圈xml
              x-apifox-orders:
                - appId
                - allowWxIds
                - atWxIds
                - disableWxIds
                - privacy
                - snsXml
              required:
                - appId
                - allowWxIds
                - atWxIds
                - disableWxIds
                - snsXml
            example:
              appId: '{{appid}}'
              allowWxIds: []
              atWxIds: []
              disableWxIds: []
              snsXml: >-
                <TimelineObject><id><![CDATA[14287710809635828232]]></id><username><![CDATA[wxid_g66c3f6y1eg922]]></username><createTime><![CDATA[1703227855]]></createTime><contentDescShowType>0</contentDescShowType><contentDescScene>0</contentDescScene><private><![CDATA[0]]></private><contentDesc></contentDesc><contentattr><![CDATA[0]]></contentattr><sourceUserName><![CDATA[]]></sourceUserName><sourceNickName><![CDATA[狮子领域
                程序圈]]></sourceNickName><statisticsData></statisticsData><weappInfo><appUserName></appUserName><pagePath></pagePath><version><![CDATA[0]]></version><isHidden>0</isHidden><debugMode><![CDATA[0]]></debugMode><shareActionId></shareActionId><isGame><![CDATA[0]]></isGame><messageExtraData></messageExtraData><subType><![CDATA[0]]></subType><preloadResources></preloadResources></weappInfo><canvasInfoXml></canvasInfoXml><ContentObject><contentStyle><![CDATA[3]]></contentStyle><contentSubStyle><![CDATA[0]]></contentSubStyle><title><![CDATA[RuoYi-Vue-Plus
                发布 5.1.2 版本 2023 最后一版]]></title><description><![CDATA[
                ]]></description><contentUrl><![CDATA[http://mp.weixin.qq.com/s?__biz=Mzg4MDYyMzQ5OQ==&mid=2247488653&idx=1&sn=4adf3b791d46d25a117368acea19bd30&chksm=cf733e69f804b77f1fc08a994c41fb76ea933200b7cd484fa8b4fee8b810b1dd78a340c4cb83&mpshare=1&scene=2&srcid=1222KNQu96XLoOwcMuphqc5q&sharer_shareinfo=9689a1855d235961b3bc8f49f788da34&sharer_shareinfo_first=9689a1855d235961b3bc8f49f788da34#rd]]></contentUrl><mediaList><media><id><![CDATA[14287710810308162053]]></id><type><![CDATA[2]]></type><title></title><description></description><private><![CDATA[0]]></private><url
                type="1"><![CDATA[http://shmmsns.qpic.cn/mmsns/C5Hh7IZThT42LQAraZkUG3bIHHicRLQeuzibCs1FqoIw0KSaQus3BleoNwvSSRcKnd200SBRM0cks/0]]></url><thumb
                type="1"><![CDATA[http://shmmsns.qpic.cn/mmsns/C5Hh7IZThT42LQAraZkUG3bIHHicRLQeuzibCs1FqoIw0KSaQus3BleoNwvSSRcKnd200SBRM0cks/150]]></thumb><videoDuration><![CDATA[0.0]]></videoDuration><size
                totalSize="3636.0" width="150.0"
                height="150.0"></size></media></mediaList><mmreadershare><itemshowtype>0</itemshowtype><ispaysubscribe>0</ispaysubscribe></mmreadershare></ContentObject><actionInfo><appMsg><mediaTagName></mediaTagName><messageExt></messageExt><messageAction></messageAction></appMsg></actionInfo><statExtStr></statExtStr><appInfo><id></id></appInfo><location
                poiClassifyId="" poiName="" poiAddress="" poiClassifyType="0"
                city=""></location><publicUserName>gh_23471f7470c1</publicUserName><streamvideo><streamvideourl></streamvideourl><streamvideothumburl></streamvideothumburl><streamvideoweburl></streamvideoweburl></streamvideo></TimelineObject>
              privacy: false
              allowTagIds: []
              disableTagIds: []
      responses:
        '200':
          description: ''
          content:
            application/json:
              schema:
                type: object
                properties:
                  ret:
                    type: integer
                  msg:
                    type: string
                  data:
                    type: object
                    properties:
                      id:
                        type: integer
                        description: 朋友圈ID
                      userName:
                        type: string
                        description: 朋友圈作者的wxid
                      nickName:
                        type: string
                        description: 朋友圈作者的昵称
                      createTime:
                        type: integer
                        description: 发布时间
                    required:
                      - id
                      - userName
                      - nickName
                      - createTime
                    x-apifox-orders:
                      - id
                      - userName
                      - nickName
                      - createTime
                required:
                  - ret
                  - msg
                  - data
                x-apifox-orders:
                  - ret
                  - msg
                  - data
              example:
                ret: 200
                msg: 操作成功
                data:
                  id: 14292805435261587000
                  userName: zhangchuan2288
                  nickName: 朝夕。
                  createTime: 1703835181
          headers: {}
          x-apifox-name: 成功
      security: []
      x-apifox-folder: 基础API/朋友圈模块
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3475559/apis/api-139908346-run
components:
  schemas: {}
  securitySchemes: {}
servers:
  - url: http://218.78.116.24:10883
    description: 测试环境
security: []

```

# 自己的朋友圈列表

## OpenAPI

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /gewe/v2/api/sns/snsList:
    post:
      summary: 自己的朋友圈列表
      deprecated: false
      description: ''
      tags:
        - 基础API/朋友圈模块
      parameters:
        - name: X-GEWE-TOKEN
          in: header
          description: ''
          required: true
          example: '{{gewe-token}}'
          schema:
            type: string
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                appId:
                  type: string
                  description: 设备ID
                  additionalProperties: false
                maxId:
                  type: number
                  description: 首次传0，第二页及以后传接口返回的maxId
                decrypt:
                  type: boolean
                  description: 是否解密
                  default: 'true'
                firstPageMd5:
                  type: string
                  description: 首次传空，第二页及以后传接口返回的firstPageMd5
              x-apifox-orders:
                - appId
                - maxId
                - decrypt
                - firstPageMd5
              required:
                - appId
            example:
              appId: '{{appid}}'
              maxId: 0
              decrypt: true
              firstPageMd5: ''
      responses:
        '200':
          description: ''
          content:
            application/json:
              schema:
                type: object
                properties:
                  ret:
                    type: integer
                  msg:
                    type: string
                  data:
                    type: object
                    properties:
                      firstPageMd5:
                        type: string
                        description: 翻页key
                      maxId:
                        type: integer
                        description: 列表最后一条的snsId
                      snsCount:
                        type: integer
                        description: 条数
                      requestTime:
                        type: integer
                        description: 请求时间
                      snsList:
                        type: array
                        items:
                          type: object
                          properties:
                            id:
                              type: integer
                              description: 朋友圈ID
                            userName:
                              type: string
                              description: 朋友圈作者的wxid
                            nickName:
                              type: string
                              description: 朋友圈作者的昵称
                            createTime:
                              type: integer
                              description: 发布时间
                            snsXml:
                              type: string
                              description: 朋友圈的xml，可用于转发朋友圈
                            likeCount:
                              type: integer
                              description: 点赞数
                            likeList:
                              type: 'null'
                              description: 点赞好友的wxid
                            commentCount:
                              type: integer
                              description: 评论数
                            commentList:
                              type: 'null'
                              description: 评论的内容
                            withUserCount:
                              type: integer
                              description: 提醒谁看的数量
                            withUserList:
                              type: 'null'
                              description: 提醒谁看的wxid
                          required:
                            - id
                            - userName
                            - nickName
                            - createTime
                            - snsXml
                            - likeCount
                            - likeList
                            - commentCount
                            - commentList
                            - withUserCount
                            - withUserList
                          x-apifox-orders:
                            - id
                            - userName
                            - nickName
                            - createTime
                            - snsXml
                            - likeCount
                            - likeList
                            - commentCount
                            - commentList
                            - withUserCount
                            - withUserList
                    required:
                      - firstPageMd5
                      - maxId
                      - snsCount
                      - requestTime
                      - snsList
                    x-apifox-orders:
                      - firstPageMd5
                      - maxId
                      - snsCount
                      - requestTime
                      - snsList
                required:
                  - ret
                  - msg
                  - data
                x-apifox-orders:
                  - ret
                  - msg
                  - data
              example:
                ret: 200
                msg: 操作成功
                data:
                  firstPageMd5: 2eb48afd4862ddc8
                  maxId: 14287734111135740000
                  snsCount: 10
                  requestTime: 1703236186
                  snsList:
                    - id: 14287779828924756000
                      userName: wxid_thd7lxtbjblp22
                      nickName: 王娇
                      createTime: 1703236082
                      snsXml: >-
                        <TimelineObject><id><![CDATA[14287779828924756671]]></id><username><![CDATA[wxid_thd7lxtbjblp22]]></username><createTime><![CDATA[1703236082]]></createTime><contentDescShowType>0</contentDescShowType><contentDescScene>0</contentDescScene><private><![CDATA[0]]></private><contentDesc><![CDATA[年化3.55
                        公积金满1000就可以办理]]></contentDesc><contentattr><![CDATA[0]]></contentattr><sourceUserName></sourceUserName><sourceNickName></sourceNickName><statisticsData></statisticsData><weappInfo><appUserName></appUserName><pagePath></pagePath><version><![CDATA[0]]></version><debugMode><![CDATA[0]]></debugMode><shareActionId></shareActionId><isGame><![CDATA[0]]></isGame><messageExtraData></messageExtraData><subType><![CDATA[0]]></subType><preloadResources></preloadResources></weappInfo><canvasInfoXml></canvasInfoXml><ContentObject><contentStyle><![CDATA[1]]></contentStyle><contentSubStyle><![CDATA[0]]></contentSubStyle><title></title><description></description><contentUrl></contentUrl><mediaList><media><id><![CDATA[14287779829602333383]]></id><type><![CDATA[2]]></type><title></title><description></description><private><![CDATA[0]]></private><url
                        type="1"
                        md5="d001e2d7e551242dc9187e71773f28cb"><![CDATA[http://shmmsns.qpic.cn/mmsns/7cM5CRSLxfDHTVo1aBzEYdpNmn8pX0dtn6ibhauZBqCibV0tm5Pf2tq6cSTnRY4icM5nN1LcCicsPiaI/0]]></url><thumb
                        type="1"><![CDATA[http://shmmsns.qpic.cn/mmsns/7cM5CRSLxfDHTVo1aBzEYdpNmn8pX0dtn6ibhauZBqCibV0tm5Pf2tq6cSTnRY4icM5nN1LcCicsPiaI/150]]></thumb><videoDuration><![CDATA[0.0]]></videoDuration><size
                        totalSize="63166.0" width="1080.0"
                        height="1440.0"></size></media></mediaList></ContentObject><actionInfo><appMsg><mediaTagName></mediaTagName><messageExt></messageExt><messageAction></messageAction></appMsg></actionInfo><appInfo><id></id></appInfo><location
                        poiClassifyId="" poiName="" poiAddress=""
                        poiClassifyType="0"
                        city=""></location><publicUserName></publicUserName><streamvideo><streamvideourl></streamvideourl><streamvideothumburl></streamvideothumburl><streamvideoweburl></streamvideoweburl></streamvideo></TimelineObject>
                      likeCount: 0
                      likeList: null
                      commentCount: 0
                      commentList: null
                      withUserCount: 0
                      withUserList: null
                    - id: 14287777324036526000
                      userName: wxid_tpnlnnvjit522
                      nickName: 任寅
                      createTime: 1703235784
                      snsXml: >-
                        <TimelineObject><id>14287777324036526701</id><username>wxid_tpnlnnvjit522</username><createTime>1703235784</createTime><contentDesc>[庆祝]新卡易贷，冰点‮回价‬馈&#x0A;[太阳]年化利率3.18%起（单利计算）&#x0A;[鼓掌]信‮额用‬度高达50万(我行房贷‮最客‬高100W)&#x0A;[礼物]可先息后本，额‮循度‬环&#x0A;[拳头]上门团办，高‮审效‬批</contentDesc><contentDescShowType>1</contentDescShowType><contentDescScene>3</contentDescScene><private>0</private><sightFolded>0</sightFolded><showFlag>0</showFlag><appInfo><id></id><version></version><appName></appName><installUrl></installUrl><fromUrl></fromUrl><isForceUpdate>0</isForceUpdate><isHidden>0</isHidden></appInfo><sourceUserName></sourceUserName><sourceNickName></sourceNickName><statisticsData></statisticsData><statExtStr></statExtStr><ContentObject><contentStyle>1</contentStyle><title></title><description></description><mediaList><media><id>14287777324490887803</id><type>2</type><title></title><description>[庆祝]新卡易贷，冰点‮回价‬馈&#x0A;[太阳]年化利率3.18%起（单利计算）&#x0A;[鼓掌]信‮额用‬度高达50万(我行房贷‮最客‬高100W)&#x0A;[礼物]可先息后本，额‮循度‬环&#x0A;[拳头]上门团办，高‮审效‬批</description><private>0</private><userData></userData><subType>0</subType><videoSize
                        width="1080" height="1947"></videoSize><url type="1"
                        md5="b790996e0ec1e961430c0e0bd1b87919"
                        videomd5="">http://shmmsns.qpic.cn/mmsns/7MykMgNAr8Ckyc5tGOdUBDDoJYI54mTHdkibYTOf5j3baZnewCPcV6Pia2wQxDkVGJb0W6Z4lH474/0</url><thumb
                        type="1">http://shmmsns.qpic.cn/mmsns/7MykMgNAr8Ckyc5tGOdUBDDoJYI54mTHdkibYTOf5j3baZnewCPcV6Pia2wQxDkVGJb0W6Z4lH474/150</thumb><size
                        width="1080.000000" height="1947.000000"
                        totalSize="77664"></size></media></mediaList><contentUrl></contentUrl></ContentObject><actionInfo><appMsg><messageAction></messageAction></appMsg></actionInfo><location
                        poiClassifyId="" poiName="" poiAddress=""
                        poiClassifyType="0"
                        city=""></location><publicUserName></publicUserName><streamvideo><streamvideourl></streamvideourl><streamvideothumburl></streamvideothumburl><streamvideoweburl></streamvideoweburl></streamvideo></TimelineObject>
                      likeCount: 0
                      likeList: null
                      commentCount: 0
                      commentList: null
                      withUserCount: 0
                      withUserList: null
                    - id: 14287770802419536000
                      userName: wxid_4mb3zx0q09fq21
                      nickName: 花笙里花艺气球  武警17772257273
                      createTime: 1703235006
                      snsXml: >-
                        <TimelineObject><id>14287770802419536384</id><username>wxid_4mb3zx0q09fq21</username><createTime>1703235006</createTime><contentDesc>客订圣诞树🎄</contentDesc><contentDescShowType>0</contentDescShowType><contentDescScene>0</contentDescScene><private>0</private><sightFolded>0</sightFolded><showFlag>0</showFlag><appInfo><id></id><version></version><appName></appName><installUrl></installUrl><fromUrl></fromUrl><isForceUpdate>0</isForceUpdate><isHidden>0</isHidden></appInfo><sourceUserName></sourceUserName><sourceNickName></sourceNickName><statisticsData></statisticsData><statExtStr></statExtStr><ContentObject><contentStyle>15</contentStyle><title>微信小视频</title><description>Sight</description><mediaList><media><id>14287770803199939062</id><type>6</type><title></title><description>客订圣诞树🎄</description><private>0</private><userData></userData><subType>0</subType><videoSize
                        width="720" height="1280"></videoSize><url type="1"
                        md5="65363e2409c934368115b3a5e25923ac"
                        videomd5="2c41a7e273e4aa9ee51a6ea7215b2609">http://shzjwxsns.video.qq.com/102/20202/snsvideodownload?filekey=30340201010420301e02016604025348041065363e2409c934368115b3a5e25923ac0203290a93040d00000004627466730000000132&amp;hy=SH&amp;storeid=565854dbd000e7ec0283837a70000006600004eea53480aa39031573aa361f&amp;dotrans=9&amp;ef=30_0&amp;bizid=1023&amp;ilogo=2&amp;dur=12&amp;upid=290110</url><thumb
                        type="1">http://vweixinthumb.tc.qq.com/150/20250/snsvideodownload?filekey=30340201010420301e02020096040253480410c310e3e2f7820dd5c9c76e76643b26dd020265d9040d00000004627466730000000132&amp;hy=SH&amp;storeid=565854dbd000d6a68283837a70000009600004f1a53482aa8cbc1e67344c31&amp;bizid=1023</thumb><size
                        width="224.000000" height="398.000000"
                        totalSize="2689683"></size><videoDuration>12.309000</videoDuration><VideoColdDLRule><All>CAISBAgWEAEoAjAc</All></VideoColdDLRule></media></mediaList><contentUrl>https://support.weixin.qq.com/cgi-bin/mmsupport-bin/readtemplate?t=page/common_page__upgrade&amp;v=1</contentUrl></ContentObject><actionInfo><appMsg><messageAction></messageAction></appMsg></actionInfo><location
                        poiClassifyId="" poiName="" poiAddress=""
                        poiClassifyType="0"
                        city=""></location><publicUserName></publicUserName><streamvideo><streamvideourl></streamvideourl><streamvideothumburl></streamvideothumburl><streamvideoweburl></streamvideoweburl></streamvideo></TimelineObject>
                      likeCount: 0
                      likeList: null
                      commentCount: 0
                      commentList: null
                      withUserCount: 0
                      withUserList: null
                    - id: 14287761219266286000
                      userName: wxid_pjhkdf7uywtd12
                      nickName: A 绿洲洗衣连锁13701469587
                      createTime: 1703233864
                      snsXml: >-
                        <TimelineObject><id>14287761219266286277</id><username>wxid_pjhkdf7uywtd12</username><createTime>1703233864</createTime><contentDesc>今天冬至，本店已下班，小伙伴们别跑空哦！</contentDesc><contentDescShowType>0</contentDescShowType><contentDescScene>3</contentDescScene><private>0</private><sightFolded>0</sightFolded><showFlag>0</showFlag><appInfo><id></id><version></version><appName></appName><installUrl></installUrl><fromUrl></fromUrl><isForceUpdate>0</isForceUpdate><isHidden>0</isHidden></appInfo><sourceUserName></sourceUserName><sourceNickName></sourceNickName><statisticsData></statisticsData><statExtStr></statExtStr><ContentObject><contentStyle>1</contentStyle><title></title><description></description><mediaList><media><id>14287761219887108802</id><type>2</type><title></title><description>今天冬至，本店已下班，小伙伴们别跑空哦！</description><private>0</private><userData></userData><subType>0</subType><videoSize
                        width="1920" height="1080"></videoSize><url type="1"
                        md5="f97e824d9af8f913bad6531b76c6f295"
                        videomd5="">http://shmmsns.qpic.cn/mmsns/PnFhfibQibZXPjibeNjjW2wLlficFiatLibNK6hDn1nicwYAIhpjUSia43yruTPRBicKwSeicJJ8OjpWloKXw/0</url><thumb
                        type="1">http://shmmsns.qpic.cn/mmsns/PnFhfibQibZXPjibeNjjW2wLlficFiatLibNK6hDn1nicwYAIhpjUSia43yruTPRBicKwSeicJJ8OjpWloKXw/150</thumb><size
                        width="1920.000000" height="1080.000000"
                        totalSize="174343"></size></media></mediaList><contentUrl></contentUrl></ContentObject><actionInfo><appMsg><messageAction></messageAction></appMsg></actionInfo><location
                        poiClassifyId="" poiName="" poiAddress=""
                        poiClassifyType="0"
                        city=""></location><publicUserName></publicUserName><streamvideo><streamvideourl></streamvideourl><streamvideothumburl></streamvideothumburl><streamvideoweburl></streamvideoweburl></streamvideo></TimelineObject>
                      likeCount: 0
                      likeList: null
                      commentCount: 0
                      commentList: null
                      withUserCount: 0
                      withUserList: null
                    - id: 14287760836481192000
                      userName: wxid_pjhkdf7uywtd12
                      nickName: A 绿洲洗衣连锁13701469587
                      createTime: 1703233818
                      snsXml: >-
                        <TimelineObject><id>14287760836481192643</id><username>wxid_pjhkdf7uywtd12</username><createTime>1703233818</createTime><contentDesc>今天4点下班，带来不便，敬请谅解！小伙伴们需要取衣服的别跑空哦！</contentDesc><contentDescShowType>0</contentDescShowType><contentDescScene>3</contentDescScene><private>0</private><sightFolded>0</sightFolded><showFlag>0</showFlag><appInfo><id></id><version></version><appName></appName><installUrl></installUrl><fromUrl></fromUrl><isForceUpdate>0</isForceUpdate><isHidden>0</isHidden></appInfo><sourceUserName></sourceUserName><sourceNickName></sourceNickName><statisticsData></statisticsData><statExtStr></statExtStr><ContentObject><contentStyle>1</contentStyle><title></title><description></description><mediaList><media><id>14287760836919038655</id><type>2</type><title></title><description>今天4点下班，带来不便，敬请谅解！小伙伴们需要取衣服的别跑空哦！</description><private>0</private><userData></userData><subType>0</subType><videoSize
                        width="1920" height="1080"></videoSize><url type="1"
                        md5="f97e824d9af8f913bad6531b76c6f295"
                        videomd5="">http://shmmsns.qpic.cn/mmsns/PnFhfibQibZXPjibeNjjW2wLodQqRg6ejEUQkwhro4CjG7NSdZMicENLrPb299Ky5HzJftV7R90MHT4/0</url><thumb
                        type="1">http://shmmsns.qpic.cn/mmsns/PnFhfibQibZXPjibeNjjW2wLodQqRg6ejEUQkwhro4CjG7NSdZMicENLrPb299Ky5HzJftV7R90MHT4/150</thumb><size
                        width="1920.000000" height="1080.000000"
                        totalSize="174343"></size></media></mediaList><contentUrl></contentUrl></ContentObject><actionInfo><appMsg><messageAction></messageAction></appMsg></actionInfo><location
                        poiClassifyId="" poiName="" poiAddress=""
                        poiClassifyType="0"
                        city=""></location><publicUserName></publicUserName><streamvideo><streamvideourl></streamvideourl><streamvideothumburl></streamvideothumburl><streamvideoweburl></streamvideoweburl></streamvideo></TimelineObject>
                      likeCount: 0
                      likeList: null
                      commentCount: 0
                      commentList: null
                      withUserCount: 0
                      withUserList: null
                    - id: 14287755418877300000
                      userName: wxid_4mb3zx0q09fq21
                      nickName: 花笙里花艺气球  武警17772257273
                      createTime: 1703233172
                      snsXml: >-
                        <TimelineObject><id>14287755418877301240</id><username>wxid_4mb3zx0q09fq21</username><createTime>1703233172</createTime><contentDesc>礼盒款来了</contentDesc><contentDescShowType>0</contentDescShowType><contentDescScene>0</contentDescScene><private>0</private><sightFolded>0</sightFolded><showFlag>0</showFlag><appInfo><id></id><version></version><appName></appName><installUrl></installUrl><fromUrl></fromUrl><isForceUpdate>0</isForceUpdate><isHidden>0</isHidden></appInfo><sourceUserName></sourceUserName><sourceNickName></sourceNickName><statisticsData></statisticsData><statExtStr></statExtStr><ContentObject><contentStyle>15</contentStyle><title>微信小视频</title><description>Sight</description><mediaList><media><id>14287755419476693503</id><type>6</type><title></title><description>礼盒款来了</description><private>0</private><userData></userData><subType>0</subType><videoSize
                        width="720" height="1280"></videoSize><url type="1"
                        md5="159a2c16de0f907ec0e9a2b620ba5588"
                        videomd5="2246b66261a58b2b2bf97345878af647">http://shzjwxsns.video.qq.com/102/20202/snsvideodownload?filekey=30340201010420301e020166040253480410159a2c16de0f907ec0e9a2b620ba558802030d2714040d00000004627466730000000132&amp;hy=SH&amp;storeid=56585469400039031283837a70000006600004eea53482fe35b00b747cb60b&amp;dotrans=1&amp;ef=30_0&amp;bizid=1023&amp;ilogo=2&amp;dur=14&amp;upid=500220</url><thumb
                        type="1">http://vweixinthumb.tc.qq.com/150/20250/snsvideodownload?filekey=30340201010420301e0202009604025348041059e68e82b666ea8762263d875c7643c3020274c0040d00000004627466730000000132&amp;hy=SH&amp;storeid=56585469400031c0e283837a70000009600004f1a53480fe3d03156924853d&amp;bizid=1023</thumb><size
                        width="224.000000" height="398.000000"
                        totalSize="861972"></size><videoDuration>14.329000</videoDuration><VideoColdDLRule><All>CAISBAgWEAEoAjAc</All></VideoColdDLRule></media></mediaList><contentUrl>https://support.weixin.qq.com/cgi-bin/mmsupport-bin/readtemplate?t=page/common_page__upgrade&amp;v=1</contentUrl></ContentObject><actionInfo><appMsg><messageAction></messageAction></appMsg></actionInfo><location
                        poiClassifyId="" poiName="" poiAddress=""
                        poiClassifyType="0"
                        city=""></location><publicUserName></publicUserName><streamvideo><streamvideourl></streamvideourl><streamvideothumburl></streamvideothumburl><streamvideoweburl></streamvideoweburl></streamvideo></TimelineObject>
                      likeCount: 0
                      likeList: null
                      commentCount: 0
                      commentList: null
                      withUserCount: 0
                      withUserList: null
                    - id: 14287752581719069000
                      userName: wxid_6ahp3voguhso21
                      nickName: 可可～
                      createTime: 1703232834
                      snsXml: >-
                        <TimelineObject><id>14287752581719069335</id><username>wxid_6ahp3voguhso21</username><createTime>1703232834</createTime><contentDesc>夏天变冬天</contentDesc><contentDescShowType>0</contentDescShowType><contentDescScene>0</contentDescScene><private>0</private><sightFolded>0</sightFolded><showFlag>0</showFlag><appInfo><id></id><version></version><appName></appName><installUrl></installUrl><fromUrl></fromUrl><isForceUpdate>0</isForceUpdate><isHidden>0</isHidden></appInfo><sourceUserName></sourceUserName><sourceNickName></sourceNickName><statisticsData></statisticsData><statExtStr></statExtStr><ContentObject><contentStyle>15</contentStyle><title>微信小视频</title><description>Sight</description><mediaList><media><id>14287752582549803671</id><type>6</type><title></title><description>夏天变冬天</description><private>0</private><userData></userData><subType>0</subType><videoSize
                        width="720" height="1280"></videoSize><url type="1"
                        md5="a06c73286db3ef0c0c726ad08a625b73"
                        videomd5="72c44f1d9c66a3a60a2b81409f9c7fa6">http://shzjwxsns.video.qq.com/102/20202/snsvideodownload?filekey=30340201010420301e020166040253480410a06c73286db3ef0c0c726ad08a625b73020337e141040d00000004627466730000000132&amp;hy=SH&amp;storeid=565854541000c6e177b359fcd0000006600004eea534802506bd1e7c5f28ea&amp;dotrans=10&amp;ef=30_0&amp;bizid=1023&amp;dur=3&amp;upid=500250</url><thumb
                        type="1">http://vweixinthumb.tc.qq.com/150/20250/snsvideodownload?filekey=30340201010420301e02020096040253480410b83b4ff949c0f0a1c7511632773a096b02027065040d00000004627466730000000132&amp;hy=SH&amp;storeid=565854541000b0f467b359fcd0000009600004f1a53480258abc1e6fc10b7a&amp;bizid=1023</thumb><size
                        width="224.000000" height="398.000000"
                        totalSize="3662145"></size><videoDuration>3.584000</videoDuration><VideoColdDLRule><All>CAISBAgWEAEoAjAc</All></VideoColdDLRule></media></mediaList><contentUrl>https://support.weixin.qq.com/cgi-bin/mmsupport-bin/readtemplate?t=page/common_page__upgrade&amp;v=1</contentUrl></ContentObject><VideoTemplate><Type>miaojian</Type><TemplateId>mv_creator_23611db0b7b54748b6e5ba97efa970ba</TemplateId><MusicId>4:1530091529305194496:1</MusicId><VersionInfo><IosSdkVersionMin>1004000</IosSdkVersionMin><AndroidSdkVersionMin>1004000</AndroidSdkVersionMin></VersionInfo></VideoTemplate><actionInfo><appMsg><messageAction></messageAction></appMsg></actionInfo><location
                        poiClassifyId="" poiName="" poiAddress=""
                        poiClassifyType="0"
                        city=""></location><publicUserName></publicUserName><streamvideo><streamvideourl></streamvideourl><streamvideothumburl></streamvideothumburl><streamvideoweburl></streamvideoweburl></streamvideo></TimelineObject>
                      likeCount: 0
                      likeList: null
                      commentCount: 0
                      commentList: null
                      withUserCount: 0
                      withUserList: null
                    - id: 14287737586012074000
                      userName: wxid_qvr1de7aqyqf22
                      nickName: 郭
                      createTime: 1703231046
                      snsXml: >-
                        <TimelineObject><id>14287737586012074529</id><username>wxid_qvr1de7aqyqf22</username><createTime>1703231046</createTime><contentDesc>这条我支持老胡。基金经理的基金涨跌与他的收入没关系是不是太搞笑了，特别现在我亏钱的情况下，一想到他们还能旱涝保收，我就特不爽，凭什么，在我们国家能旱涝保收的只有一个职业。</contentDesc><contentDescShowType>0</contentDescShowType><contentDescScene>3</contentDescScene><private>0</private><sightFolded>0</sightFolded><showFlag>0</showFlag><appInfo><id></id><version></version><appName></appName><installUrl></installUrl><fromUrl></fromUrl><isForceUpdate>0</isForceUpdate></appInfo><sourceUserName></sourceUserName><sourceNickName></sourceNickName><statisticsData></statisticsData><statExtStr></statExtStr><ContentObject><contentStyle>1</contentStyle><title></title><description></description><mediaList><media><id>14287737586445726298</id><type>2</type><title></title><description>这条我支持老胡。基金经理的基金涨跌与他的收入没关系是不是太搞笑了，特别现在我亏钱的情况下，一想到他们还能旱涝保收，我就特不爽，凭什么，在我们国家能旱涝保收的只有一个职业。</description><private>0</private><userData></userData><subType>0</subType><videoSize
                        width="1886" height="1144"></videoSize><url type="1"
                        md5="99f448140dc861412a73a46cae7b70d3"
                        videomd5="">http://szmmsns.qpic.cn/mmsns/iaaSC1CuspWQI4kia9ulvp3FxkL8LcSjtiannMll3oBjj208ApMAAe1iaBl2kFlBum4XTG4h4buSCLE/0</url><thumb
                        type="1">http://szmmsns.qpic.cn/mmsns/iaaSC1CuspWQI4kia9ulvp3FxkL8LcSjtiannMll3oBjj208ApMAAe1iaBl2kFlBum4XTG4h4buSCLE/150</thumb><size
                        width="1780.000000" height="1080.000000"
                        totalSize="111771"></size></media></mediaList><contentUrl></contentUrl></ContentObject><actionInfo><appMsg><messageAction></messageAction></appMsg></actionInfo><location
                        poiClassifyId="" poiName="" poiAddress=""
                        poiClassifyType="0"
                        city=""></location><publicUserName></publicUserName><streamvideo><streamvideourl></streamvideourl><streamvideothumburl></streamvideothumburl><streamvideoweburl></streamvideoweburl></streamvideo></TimelineObject>
                      likeCount: 0
                      likeList: null
                      commentCount: 0
                      commentList: null
                      withUserCount: 0
                      withUserList: null
                    - id: 14287736959729742000
                      userName: wxid_ypzeeovk3r0d22
                      nickName: 马士兵教育~洁如（14:00-23:00）
                      createTime: 1703230972
                      snsXml: >-
                        <TimelineObject><id><![CDATA[14287736959729742329]]></id><username><![CDATA[wxid_ypzeeovk3r0d22]]></username><createTime><![CDATA[1703230972]]></createTime><contentDescShowType>0</contentDescShowType><contentDescScene>0</contentDescScene><private><![CDATA[0]]></private><contentDesc><![CDATA[还在纠结的同学，抓紧上了[呲牙][呲牙][呲牙]]]></contentDesc><contentattr><![CDATA[0]]></contentattr><sourceUserName></sourceUserName><sourceNickName></sourceNickName><statisticsData></statisticsData><weappInfo><appUserName></appUserName><pagePath></pagePath><version><![CDATA[0]]></version><isHidden>0</isHidden><debugMode><![CDATA[0]]></debugMode><shareActionId></shareActionId><isGame><![CDATA[0]]></isGame><messageExtraData></messageExtraData><subType><![CDATA[0]]></subType><preloadResources></preloadResources></weappInfo><canvasInfoXml></canvasInfoXml><ContentObject><contentStyle><![CDATA[1]]></contentStyle><contentSubStyle><![CDATA[0]]></contentSubStyle><title></title><description></description><contentUrl></contentUrl><mediaList><media><id><![CDATA[14287736960327627271]]></id><type><![CDATA[2]]></type><title></title><description></description><private><![CDATA[0]]></private><url
                        type="1"
                        md5="349614433ba258bd41d25626c098c6cd"><![CDATA[http://shmmsns.qpic.cn/mmsns/4owBl1bibWAeYSXAZSHmJ9bHVwUg8nhvAuicR2o0ZR50OYs97cIVI6lJic3O9C9kQv7SBN3miaVwsAw/0]]></url><thumb
                        type="1"><![CDATA[http://shmmsns.qpic.cn/mmsns/4owBl1bibWAeYSXAZSHmJ9bHVwUg8nhvAuicR2o0ZR50OYs97cIVI6lJic3O9C9kQv7SBN3miaVwsAw/150]]></thumb><videoDuration><![CDATA[0.0]]></videoDuration><size
                        totalSize="26716.0" width="753.0"
                        height="557.0"></size></media></mediaList></ContentObject><actionInfo><appMsg><mediaTagName></mediaTagName><messageExt></messageExt><messageAction></messageAction></appMsg></actionInfo><appInfo><id></id></appInfo><location
                        poiClassifyId="" poiName="" poiAddress=""
                        poiClassifyType="0"
                        city=""></location><publicUserName></publicUserName><streamvideo><streamvideourl></streamvideourl><streamvideothumburl></streamvideothumburl><streamvideoweburl></streamvideoweburl></streamvideo></TimelineObject>
                      likeCount: 0
                      likeList: null
                      commentCount: 0
                      commentList: null
                      withUserCount: 0
                      withUserList: null
                    - id: 14287734111135740000
                      userName: wxid_ypzeeovk3r0d22
                      nickName: 马士兵教育~洁如（14:00-23:00）
                      createTime: 1703230632
                      snsXml: >-
                        <TimelineObject><id><![CDATA[14287734111135740417]]></id><username><![CDATA[wxid_ypzeeovk3r0d22]]></username><createTime><![CDATA[1703230632]]></createTime><contentDescShowType>0</contentDescShowType><contentDescScene>0</contentDescScene><private><![CDATA[0]]></private><contentDesc><![CDATA[[烟花]新鲜出炉

                        [爱心]坐标：杭州，入职阿里

                        [赞]薪资：21k到28K，16薪

                        [加油]跟MCA课程学，好offer在手]]></contentDesc><contentattr><![CDATA[0]]></contentattr><sourceUserName></sourceUserName><sourceNickName></sourceNickName><statisticsData></statisticsData><weappInfo><appUserName></appUserName><pagePath></pagePath><version><![CDATA[0]]></version><isHidden>0</isHidden><debugMode><![CDATA[0]]></debugMode><shareActionId></shareActionId><isGame><![CDATA[0]]></isGame><messageExtraData></messageExtraData><subType><![CDATA[0]]></subType><preloadResources></preloadResources></weappInfo><canvasInfoXml></canvasInfoXml><ContentObject><contentStyle><![CDATA[1]]></contentStyle><contentSubStyle><![CDATA[0]]></contentSubStyle><title></title><description></description><contentUrl></contentUrl><mediaList><media><id><![CDATA[14287734111755645433]]></id><type><![CDATA[2]]></type><title></title><description></description><private><![CDATA[0]]></private><url
                        type="1"
                        md5="e4d93ca26eb1141e4c50a9003aef4a7c"><![CDATA[http://shmmsns.qpic.cn/mmsns/4owBl1bibWAeYSXAZSHmJ9WDU03mTNqR5mMZ1072L4evF9heJibic75FxbibCt6Da6UdYQHibMgaxghU/0]]></url><thumb
                        type="1"><![CDATA[http://shmmsns.qpic.cn/mmsns/4owBl1bibWAeYSXAZSHmJ9WDU03mTNqR5mMZ1072L4evF9heJibic75FxbibCt6Da6UdYQHibMgaxghU/150]]></thumb><videoDuration><![CDATA[0.0]]></videoDuration><size
                        totalSize="32735.0" width="1200.0"
                        height="675.0"></size></media></mediaList></ContentObject><actionInfo><appMsg><mediaTagName></mediaTagName><messageExt></messageExt><messageAction></messageAction></appMsg></actionInfo><appInfo><id></id></appInfo><location
                        poiClassifyId="" poiName="" poiAddress=""
                        poiClassifyType="0"
                        city=""></location><publicUserName></publicUserName><streamvideo><streamvideourl></streamvideourl><streamvideothumburl></streamvideothumburl><streamvideoweburl></streamvideoweburl></streamvideo></TimelineObject>
                      likeCount: 0
                      likeList: null
                      commentCount: 0
                      commentList: null
                      withUserCount: 0
                      withUserList: null
          headers: {}
          x-apifox-name: 成功
      security: []
      x-apifox-folder: 基础API/朋友圈模块
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3475559/apis/api-139908347-run
components:
  schemas: {}
  securitySchemes: {}
servers:
  - url: http://218.78.116.24:10883
    description: 测试环境
security: []

```

# 联系人的朋友圈列表

## OpenAPI

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /gewe/v2/api/sns/contactsSnsList:
    post:
      summary: 联系人的朋友圈列表
      deprecated: false
      description: ''
      tags:
        - 基础API/朋友圈模块
      parameters:
        - name: X-GEWE-TOKEN
          in: header
          description: ''
          required: true
          example: '{{gewe-token}}'
          schema:
            type: string
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                appId:
                  type: string
                  description: 设备ID
                  additionalProperties: false
                wxid:
                  type: string
                  description: 好友wxid
                maxId:
                  type: number
                  description: 首次传0，第二页及以后传接口返回的maxId
                decrypt:
                  type: boolean
                  description: 是否解密
                  default: 'true'
                firstPageMd5:
                  type: string
                  description: 首次传空，第二页及以后传接口返回的firstPageMd5
              x-apifox-orders:
                - appId
                - maxId
                - decrypt
                - wxid
                - firstPageMd5
              required:
                - appId
                - wxid
            example:
              appId: '{{appid}}'
              maxId: 0
              decrypt: true
              wxid: zhangchuan2288
              firstPageMd5: ''
      responses:
        '200':
          description: ''
          content:
            application/json:
              schema:
                type: object
                properties:
                  ret:
                    type: integer
                    additionalProperties: false
                  msg:
                    type: string
                    additionalProperties: false
                  data:
                    type: object
                    properties:
                      firstPageMd5:
                        type: string
                        description: 翻页key
                        additionalProperties: false
                      maxId:
                        type: integer
                        description: 列表最后一条的snsId
                        additionalProperties: false
                      snsCount:
                        type: integer
                        description: 条数
                        additionalProperties: false
                      requestTime:
                        type: integer
                        description: 请求时间
                        additionalProperties: false
                      snsList:
                        type: array
                        items:
                          type: object
                          properties:
                            id:
                              type: integer
                              description: 朋友圈ID
                              additionalProperties: false
                            userName:
                              type: string
                              description: 朋友圈作者的wxid
                              additionalProperties: false
                            nickName:
                              type: string
                              description: 朋友圈作者的昵称
                              additionalProperties: false
                            createTime:
                              type: integer
                              description: 发布时间
                              additionalProperties: false
                            snsXml:
                              type: string
                              description: 朋友圈的xml，可用于转发朋友圈
                              additionalProperties: false
                            likeCount:
                              type: integer
                              description: 点赞数
                              additionalProperties: false
                            likeList:
                              type: 'null'
                              description: 点赞好友的信息
                              additionalProperties: false
                            commentCount:
                              type: integer
                              description: 评论数
                              additionalProperties: false
                            commentList:
                              type: 'null'
                              description: 评论的内容
                              additionalProperties: false
                            withUserCount:
                              type: integer
                              description: 提醒谁看的数量
                              additionalProperties: false
                            withUserList:
                              type: 'null'
                              description: 提醒谁看的wxid
                              additionalProperties: false
                          required:
                            - id
                            - userName
                            - nickName
                            - createTime
                            - snsXml
                            - likeCount
                            - likeList
                            - commentCount
                            - commentList
                            - withUserCount
                            - withUserList
                          x-apifox-orders:
                            - id
                            - userName
                            - nickName
                            - createTime
                            - snsXml
                            - likeCount
                            - likeList
                            - commentCount
                            - commentList
                            - withUserCount
                            - withUserList
                    required:
                      - firstPageMd5
                      - maxId
                      - snsCount
                      - requestTime
                      - snsList
                    x-apifox-orders:
                      - firstPageMd5
                      - maxId
                      - snsCount
                      - requestTime
                      - snsList
                required:
                  - ret
                  - msg
                  - data
                x-apifox-orders:
                  - ret
                  - msg
                  - data
              example:
                ret: 200
                msg: 操作成功
                data:
                  firstPageMd5: 5b6cd464e80df435
                  maxId: 14020472144428995000
                  snsCount: 10
                  requestTime: 1703833537
                  snsList:
                    - id: 14214000407987818000
                      userName: zhangchuan2288
                      nickName: 朝夕。
                      createTime: 1694440890
                      snsXml: >-
                        <TimelineObject><id>14214000407987819068</id><username>zhangchuan2288</username><createTime>1694440890</createTime><contentDesc>搁置了一个月的战车，出门蹬一会被撞了，忘了躺地上，错失一个换车的机会。[苦涩][苦涩]</contentDesc><contentDescShowType>0</contentDescShowType><contentDescScene>3</contentDescScene><private>0</private><sightFolded>0</sightFolded><showFlag>0</showFlag><appInfo><id></id><version></version><appName></appName><installUrl></installUrl><fromUrl></fromUrl><isForceUpdate>0</isForceUpdate><isHidden>0</isHidden></appInfo><sourceUserName></sourceUserName><sourceNickName></sourceNickName><statisticsData></statisticsData><statExtStr></statExtStr><ContentObject><contentStyle>1</contentStyle><title></title><description></description><mediaList><media><id>14214000408859710018</id><type>2</type><title></title><description>搁置了一个月的战车，出门蹬一会被撞了，忘了躺地上，错失一个换车的机会。[苦涩][苦涩]</description><private>0</private><userData></userData><subType>0</subType><videoSize
                        width="1080" height="1920"></videoSize><url type="1"
                        md5="a9a21ec7afe3a51e1635cd4844de29bb"
                        videomd5="">http://shmmsns.qpic.cn/mmsns/FzeKA69P5uIdqPfQxp59LpevPpX0bJz1zbXSpiavc01kia9H4cic0dJbHbUEJDibB8jx2oXfnBuKhgg/0</url><thumb
                        type="1">http://shmmsns.qpic.cn/mmsns/FzeKA69P5uIdqPfQxp59LpevPpX0bJz1zbXSpiavc01kia9H4cic0dJbHbUEJDibB8jx2oXfnBuKhgg/150</thumb><size
                        width="1080.000000" height="1920.000000"
                        totalSize="223727"></size></media></mediaList><contentUrl></contentUrl></ContentObject><actionInfo><appMsg><messageAction></messageAction></appMsg></actionInfo><location
                        poiClassifyId="" poiName="" poiAddress=""
                        poiClassifyType="0"
                        city=""></location><publicUserName></publicUserName><streamvideo><streamvideourl></streamvideourl><streamvideothumburl></streamvideothumburl><streamvideoweburl></streamvideoweburl></streamvideo></TimelineObject>
                      likeCount: 4
                      likeList:
                        - userName: wxid_fym4i76rk40x12
                          nickName: 糖果
                          source: 0
                          type: 1
                          createTime: 1694440920
                        - userName: wxid_bhf0vdaei64u21
                          nickName: 挽风～
                          source: 0
                          type: 1
                          createTime: 1694441103
                        - userName: wxid_jcllrz90yht022
                          nickName: ^^辻弌^^
                          source: 0
                          type: 1
                          createTime: 1694441218
                        - userName: wxid_5hafab2a85yk12
                          nickName: 丶zoū zoú zoǔ zoù 👾
                          source: 0
                          type: 1
                          createTime: 1694455325
                      commentCount: 19
                      commentList:
                        - userName: wxid_6xi2yuy30id422
                          nickName: ME
                          source: 0
                          type: 2
                          content: 去医院验伤 索赔
                          createTime: 1694441070
                          commentId: 1
                          replyCommentId: 0
                          isNotRichText: 1
                        - userName: wxid_7538985368812
                          nickName: 故事的小黄花
                          source: 0
                          type: 2
                          content: 懂车帝没下载好？
                          createTime: 1694441111
                          commentId: 33
                          replyCommentId: 0
                          isNotRichText: 1
                        - userName: zhangchuan2288
                          nickName: 朝夕。
                          source: 0
                          type: 2
                          content: 来不及了，赔了点钱就让走了[捂脸]
                          createTime: 1694441270
                          commentId: 65
                          replyCommentId: 1
                          isNotRichText: 1
                        - userName: wxid_bhf0vdaei64u21
                          nickName: 挽风～
                          source: 0
                          type: 2
                          content: 对方在想:那人竟然没躺地上，感觉他像自己赚了一个亿那么开心[破涕为笑]
                          createTime: 1694441274
                          commentId: 97
                          replyCommentId: 0
                          isNotRichText: 1
                        - userName: wxid_6xi2yuy30id422
                          nickName: ME
                          source: 0
                          type: 2
                          content: 报警 你说验出严重的伤了
                          createTime: 1694441302
                          commentId: 129
                          replyCommentId: 65
                          isNotRichText: 1
                        - userName: zhangchuan2288
                          nickName: 朝夕。
                          source: 0
                          type: 2
                          content: 没来得及，错失良机
                          createTime: 1694441314
                          commentId: 161
                          replyCommentId: 33
                          isNotRichText: 1
                        - userName: zhangchuan2288
                          nickName: 朝夕。
                          source: 0
                          type: 2
                          content: 我都看出来他的开心了😃
                          createTime: 1694441371
                          commentId: 193
                          replyCommentId: 97
                          isNotRichText: 1
                        - userName: zhangchuan2288
                          nickName: 朝夕。
                          source: 0
                          type: 2
                          content: 就是影响心情，倒是也没啥
                          createTime: 1694441407
                          commentId: 225
                          replyCommentId: 129
                          isNotRichText: 1
                        - userName: wxid_nasqrofbjvxa22
                          nickName: 灼
                          source: 0
                          type: 2
                          content: 车胎昨天刚爆[捂脸]
                          createTime: 1694441828
                          commentId: 259
                          replyCommentId: 0
                          isNotRichText: 1
                        - userName: zhangchuan2288
                          nickName: 朝夕。
                          source: 0
                          type: 2
                          content: 正好歇着
                          createTime: 1694442074
                          commentId: 289
                          replyCommentId: 259
                          isNotRichText: 1
                        - userName: wxid_98pjjzpiisi721
                          nickName: 宋端雅
                          source: 0
                          type: 2
                          content: 去医院，你有保险，咱不怕
                          createTime: 1694442081
                          commentId: 321
                          replyCommentId: 0
                          isNotRichText: 1
                        - userName: zhangchuan2288
                          nickName: 朝夕。
                          source: 0
                          type: 2
                          content: 忘了这茬。有没有自行车险，我买一个[破涕为笑][破涕为笑]
                          createTime: 1694442193
                          commentId: 353
                          replyCommentId: 321
                          isNotRichText: 1
                        - userName: wxid_98pjjzpiisi721
                          nickName: 宋端雅
                          source: 0
                          type: 2
                          content: 价值太低了，不值当的[捂脸]
                          createTime: 1694442243
                          commentId: 385
                          replyCommentId: 353
                          isNotRichText: 1
                        - userName: wxid_nasqrofbjvxa22
                          nickName: 灼
                          source: 0
                          type: 2
                          content: 一个月爆了两次[苦涩]，都没法看小姑娘了
                          createTime: 1694442381
                          commentId: 419
                          replyCommentId: 289
                          isNotRichText: 1
                        - userName: zhangchuan2288
                          nickName: 朝夕。
                          source: 0
                          type: 2
                          content: 哪有小姑娘，我骑共享单车也得去
                          createTime: 1694442448
                          commentId: 449
                          replyCommentId: 419
                          isNotRichText: 1
                        - userName: wxid_nasqrofbjvxa22
                          nickName: 灼
                          source: 0
                          type: 2
                          content: 金龙湖，大龙湖，你来
                          createTime: 1694442524
                          commentId: 483
                          replyCommentId: 449
                          isNotRichText: 1
                        - userName: wxid_5042230422112
                          nickName: 文强
                          source: 0
                          type: 2
                          content: 我看你胖了，是把车轱辘压拍圈了吧
                          createTime: 1694488063
                          commentId: 513
                          replyCommentId: 0
                          isNotRichText: 1
                        - userName: zhangchuan2288
                          nickName: 朝夕。
                          source: 0
                          type: 2
                          content: 哎日，几年不见了，你不能来请我吃个饭吗
                          createTime: 1694488128
                          commentId: 545
                          replyCommentId: 513
                          isNotRichText: 1
                        - userName: wxid_5042230422112
                          nickName: 文强
                          source: 0
                          type: 2
                          content: 你个哪了
                          createTime: 1694488297
                          commentId: 577
                          replyCommentId: 545
                          isNotRichText: 1
                      withUserCount: 0
                      withUserList: null
                    - id: 14208277753875796000
                      userName: zhangchuan2288
                      nickName: 朝夕。
                      createTime: 1693758696
                      snsXml: >-
                        <TimelineObject><id>14208277753875796533</id><username>zhangchuan2288</username><createTime>1693758696</createTime><contentDesc>家门口的音乐节总要支持一下[旺柴]</contentDesc><contentDescShowType>0</contentDescShowType><contentDescScene>3</contentDescScene><private>0</private><sightFolded>0</sightFolded><showFlag>0</showFlag><appInfo><id></id><version></version><appName></appName><installUrl></installUrl><fromUrl></fromUrl><isForceUpdate>0</isForceUpdate><isHidden>0</isHidden></appInfo><sourceUserName></sourceUserName><sourceNickName></sourceNickName><statisticsData></statisticsData><statExtStr></statExtStr><ContentObject><contentStyle>1</contentStyle><title></title><description></description><mediaList><media><id>14208277754493801017</id><type>2</type><title></title><description>家门口的音乐节总要支持一下[旺柴]</description><private>0</private><userData></userData><subType>0</subType><videoSize
                        width="4032" height="3024"></videoSize><url type="1"
                        md5="4d92355ce00a69a285fbaacc1fb87235"
                        videomd5="">http://shmmsns.qpic.cn/mmsns/FzeKA69P5uIdqPfQxp59LpoVDy1G6vico1v9waHyDEl9jAnE0BM4VTe36JnQX47MaNfiad3qFErmA/0</url><thumb
                        type="1">http://shmmsns.qpic.cn/mmsns/FzeKA69P5uIdqPfQxp59LpoVDy1G6vico1v9waHyDEl9jAnE0BM4VTe36JnQX47MaNfiad3qFErmA/150</thumb><size
                        width="1440.000000" height="1080.000000"
                        totalSize="155916"></size></media><media><id>14208277754512347715</id><type>2</type><title></title><description></description><private>0</private><userData></userData><subType>0</subType><videoSize
                        width="4032" height="3024"></videoSize><url type="1"
                        md5="93805b62afce77664432bd42da707197"
                        videomd5="">http://shmmsns.qpic.cn/mmsns/FzeKA69P5uIdqPfQxp59LpoVDy1G6vicoMsvmIUmgPSHJvfuTvX8zlezQZiaf8tmuvb4oajtczSUU/0</url><thumb
                        type="1">http://shmmsns.qpic.cn/mmsns/FzeKA69P5uIdqPfQxp59LpoVDy1G6vicoMsvmIUmgPSHJvfuTvX8zlezQZiaf8tmuvb4oajtczSUU/150</thumb><size
                        width="1440.000000" height="1080.000000"
                        totalSize="109173"></size></media><media><id>14208277754523095615</id><type>2</type><title></title><description></description><private>0</private><userData></userData><subType>0</subType><videoSize
                        width="4032" height="3024"></videoSize><url type="1"
                        md5="f51013498cd7d9e53da00d4711117c24"
                        videomd5="">http://shmmsns.qpic.cn/mmsns/FzeKA69P5uIdqPfQxp59LpoVDy1G6vicoib5UxwljGHSAaYGyUUum0ia0XpiamvtbYnwNiaJbex9COKc/0</url><thumb
                        type="1">http://shmmsns.qpic.cn/mmsns/FzeKA69P5uIdqPfQxp59LpoVDy1G6vicoib5UxwljGHSAaYGyUUum0ia0XpiamvtbYnwNiaJbex9COKc/150</thumb><size
                        width="1440.000000" height="1080.000000"
                        totalSize="25581"></size></media><media><id>14208277754538037822</id><type>2</type><title></title><description></description><private>0</private><userData></userData><subType>0</subType><videoSize
                        width="2954" height="3675"></videoSize><url type="1"
                        md5="620712b48f108661d376da70e86080dc"
                        videomd5="">http://shmmsns.qpic.cn/mmsns/FzeKA69P5uIdqPfQxp59LpoVDy1G6vicoVia0ibt106s3VZlj2uwYgaPWDUjy9BpvbuZ8G3Fptojlw/0</url><thumb
                        type="1">http://shmmsns.qpic.cn/mmsns/FzeKA69P5uIdqPfQxp59LpoVDy1G6vicoVia0ibt106s3VZlj2uwYgaPWDUjy9BpvbuZ8G3Fptojlw/150</thumb><size
                        width="1080.000000" height="1344.000000"
                        totalSize="92949"></size></media><media><id>14208277754554225206</id><type>2</type><title></title><description></description><private>0</private><userData></userData><subType>0</subType><videoSize
                        width="844" height="532"></videoSize><url type="1"
                        md5="2763fbc86db233e000893f7800d22ae0"
                        videomd5="">http://shmmsns.qpic.cn/mmsns/FzeKA69P5uIdqPfQxp59LpoVDy1G6vico75qcUzI3g9OQ2tyDicmramD6iaRibPjd2MeicaHVWjZa0nI/0</url><thumb
                        type="1">http://shmmsns.qpic.cn/mmsns/FzeKA69P5uIdqPfQxp59LpoVDy1G6vico75qcUzI3g9OQ2tyDicmramD6iaRibPjd2MeicaHVWjZa0nI/150</thumb><size
                        width="844.000000" height="532.000000"
                        totalSize="16133"></size></media><media><id>14208277754564645437</id><type>2</type><title></title><description></description><private>0</private><userData></userData><subType>0</subType><videoSize
                        width="4032" height="3024"></videoSize><url type="1"
                        md5="e4bb6e50fe77634482fb08e22948c88d"
                        videomd5="">http://shmmsns.qpic.cn/mmsns/FzeKA69P5uIdqPfQxp59LpoVDy1G6vicoAkMpJrc0SdNfZ1DRQjXWqQf8yIEs50cdDic2uxXP01F8/0</url><thumb
                        type="1">http://shmmsns.qpic.cn/mmsns/FzeKA69P5uIdqPfQxp59LpoVDy1G6vicoAkMpJrc0SdNfZ1DRQjXWqQf8yIEs50cdDic2uxXP01F8/150</thumb><size
                        width="1440.000000" height="1080.000000"
                        totalSize="49965"></size></media></mediaList><contentUrl></contentUrl></ContentObject><actionInfo><appMsg><messageAction></messageAction></appMsg></actionInfo><location
                        poiClassifyId="" poiName="" poiAddress=""
                        poiClassifyType="0"
                        city=""></location><publicUserName></publicUserName><streamvideo><streamvideourl></streamvideourl><streamvideothumburl></streamvideothumburl><streamvideoweburl></streamvideoweburl></streamvideo></TimelineObject>
                      likeCount: 18
                      likeList:
                        - userName: zhangchuan2288
                          nickName: 朝夕。
                          source: 0
                          type: 1
                          createTime: 1693758719
                        - userName: wxid_fym4i76rk40x12
                          nickName: 糖果
                          source: 0
                          type: 1
                          createTime: 1693758752
                        - userName: wxid_cy6buf12nf6921
                          nickName: 暖心
                          source: 0
                          type: 1
                          createTime: 1693758848
                        - userName: wxid_3o3fb2whu7tx22
                          nickName: 沧海候鸟
                          source: 0
                          type: 1
                          createTime: 1693759534
                        - userName: wxid_i6qsbbjenjuj22
                          nickName: Mr李
                          source: 0
                          type: 1
                          createTime: 1693762812
                        - userName: wxid_o2m8xm71c23522
                          nickName: Sunny girl🌼
                          source: 0
                          type: 1
                          createTime: 1693764342
                        - userName: wxid_lc3dkf5qserf22
                          nickName: Ch.
                          source: 0
                          type: 1
                          createTime: 1693764442
                        - userName: wxid_0rp825czl4o722
                          nickName: 小小晴仔🐳
                          source: 0
                          type: 1
                          createTime: 1693774829
                        - userName: wxid_j5zo70ve13ad22
                          nickName: A刘腾A
                          source: 0
                          type: 1
                          createTime: 1693778449
                        - userName: wxid_e4ieiqx66ose21
                          nickName: 王路
                          source: 0
                          type: 1
                          createTime: 1693780908
                        - userName: wxid_ihhaqc6dki3b22
                          nickName: 永不放弃
                          source: 0
                          type: 1
                          createTime: 1693781785
                        - userName: star911128
                          nickName: 🐑咩咩🐭咪吖🐒
                          source: 0
                          type: 1
                          createTime: 1693786930
                        - userName: wxid_3866478839212
                          nickName: 群青
                          source: 0
                          type: 1
                          createTime: 1693787156
                        - userName: wxid_jcllrz90yht022
                          nickName: ^^辻弌^^
                          source: 0
                          type: 1
                          createTime: 1693787189
                        - userName: wxid_ruqfsd3649lm12
                          nickName: 奔跑的子弹
                          source: 0
                          type: 1
                          createTime: 1693787766
                        - userName: wxid_306am6wo0bug21
                          nickName: JUST DO IT
                          source: 0
                          type: 1
                          createTime: 1693788096
                        - userName: wxid_uqg73ps26e1w22
                          nickName: 江苏水蓝.张传飞
                          source: 0
                          type: 1
                          createTime: 1693791225
                        - userName: wxid_xoy6vmt3hua622
                          nickName: _C_
                          source: 0
                          type: 1
                          createTime: 1693808488
                      commentCount: 8
                      commentList:
                        - userName: wxid_pw89aeo8dbu621
                          nickName: 凪卄
                          source: 0
                          type: 2
                          content: 咋脸那么大
                          createTime: 1693758905
                          commentId: 1
                          replyCommentId: 0
                          isNotRichText: 1
                        - userName: zhangchuan2288
                          nickName: 朝夕。
                          source: 0
                          type: 2
                          content: 是的，朴树也该减肥了
                          createTime: 1693758974
                          commentId: 33
                          replyCommentId: 1
                          isNotRichText: 1
                        - userName: wodeweixin_vip
                          nickName: 那些你很冒险的梦
                          source: 0
                          type: 2
                          content: 你家在潘安湖？
                          createTime: 1693759044
                          commentId: 65
                          replyCommentId: 0
                          isNotRichText: 1
                        - userName: zhangchuan2288
                          nickName: 朝夕。
                          source: 0
                          type: 2
                          content: 距离十几公里[破涕为笑]
                          createTime: 1693759125
                          commentId: 97
                          replyCommentId: 65
                          isNotRichText: 1
                        - userName: wxid_ihhaqc6dki3b22
                          nickName: 永不放弃
                          source: 0
                          type: 2
                          content: 儿子再增加些笑容，就更好了。
                          createTime: 1693782120
                          commentId: 131
                          replyCommentId: 0
                          isNotRichText: 1
                        - userName: zhangchuan2288
                          nickName: 朝夕。
                          source: 0
                          type: 2
                          content: '[笑脸][笑脸]'
                          createTime: 1693791930
                          commentId: 161
                          replyCommentId: 131
                          isNotRichText: 1
                        - userName: wxid_xoy6vmt3hua622
                          nickName: _C_
                          source: 0
                          type: 2
                          content: 周末不加班你跑去喂蚊子[旺柴]
                          createTime: 1693808512
                          commentId: 195
                          replyCommentId: 0
                          isNotRichText: 1
                        - userName: zhangchuan2288
                          nickName: 朝夕。
                          source: 0
                          type: 2
                          content: 音乐节上敲代码你是没看到
                          createTime: 1693811409
                          commentId: 225
                          replyCommentId: 195
                          isNotRichText: 1
                      withUserCount: 0
                      withUserList: null
                    - id: 14181924094520332000
                      userName: zhangchuan2288
                      nickName: 朝夕。
                      createTime: 1690617095
                      snsXml: >-
                        <TimelineObject><id>14181924094520332866</id><username>zhangchuan2288</username><createTime>1690617095</createTime><contentDesc>绿色出行</contentDesc><contentDescShowType>0</contentDescShowType><contentDescScene>3</contentDescScene><private>0</private><sightFolded>0</sightFolded><showFlag>0</showFlag><location
                        city="徐州市" longitude="117.150677" latitude="34.263137"
                        poiName="徐州市 · 云龙湖风景名胜区" poiAddress="金山南路与湖南路交叉口西侧"
                        poiScale="11.000000" poiInfoUrl=""
                        poiClassifyId="qqmap_1794642106729631519"
                        poiClassifyType="1" poiClickableStatus="0"
                        buildingId="0" floorName="" poiAddressName="云龙湖风景名胜区"
                        country="中国"></location><appInfo><id></id><version></version><appName></appName><installUrl></installUrl><fromUrl></fromUrl><isForceUpdate>0</isForceUpdate><isHidden>0</isHidden></appInfo><sourceUserName></sourceUserName><sourceNickName></sourceNickName><statisticsData></statisticsData><statExtStr></statExtStr><ContentObject><contentStyle>1</contentStyle><title></title><description></description><mediaList><media><id>14181924095134929470</id><type>2</type><title></title><description>绿色出行</description><private>0</private><userData></userData><subType>0</subType><videoSize
                        width="4032" height="3024"></videoSize><url type="1"
                        md5="69f0633b014da2f276d3010dc72bfdb9"
                        videomd5="">http://shmmsns.qpic.cn/mmsns/FzeKA69P5uIdqPfQxp59LjOTlD15KTEicdd6ThtD27thg3MOiaquV0UrJCaVaLDQ5gnIrgBkFAWbA/0</url><thumb
                        type="1">http://shmmsns.qpic.cn/mmsns/FzeKA69P5uIdqPfQxp59LjOTlD15KTEicdd6ThtD27thg3MOiaquV0UrJCaVaLDQ5gnIrgBkFAWbA/150</thumb><size
                        width="1440.000000" height="1080.000000"
                        totalSize="98836"></size></media><media><id>14181924095154197055</id><type>2</type><title></title><description></description><private>0</private><userData></userData><subType>0</subType><videoSize
                        width="4032" height="3024"></videoSize><url type="1"
                        md5="9bdca5d50e7f45144a67e6d29f53e238"
                        videomd5="">http://shmmsns.qpic.cn/mmsns/FzeKA69P5uIdqPfQxp59LjOTlD15KTEic4VlibNthFibR2uH5QoWGkWDkIDBFUB59vxiaRKiaSiaIYcx8/0</url><thumb
                        type="1">http://shmmsns.qpic.cn/mmsns/FzeKA69P5uIdqPfQxp59LjOTlD15KTEic4VlibNthFibR2uH5QoWGkWDkIDBFUB59vxiaRKiaSiaIYcx8/150</thumb><size
                        width="1440.000000" height="1080.000000"
                        totalSize="96792"></size></media></mediaList><contentUrl></contentUrl></ContentObject><actionInfo><appMsg><messageAction></messageAction></appMsg></actionInfo><publicUserName></publicUserName><streamvideo><streamvideourl></streamvideourl><streamvideothumburl></streamvideothumburl><streamvideoweburl></streamvideoweburl></streamvideo></TimelineObject>
                      likeCount: 2
                      likeList:
                        - userName: wxid_3o3fb2whu7tx22
                          nickName: 沧海候鸟
                          source: 0
                          type: 1
                          createTime: 1690620790
                        - userName: wxid_0rp825czl4o722
                          nickName: 小小晴仔🐳
                          source: 0
                          type: 1
                          createTime: 1690668464
                      commentCount: 14
                      commentList:
                        - userName: wxid_pw89aeo8dbu621
                          nickName: 恰巧经过。
                          source: 0
                          type: 2
                          content: 来爬山
                          createTime: 1690617182
                          commentId: 1
                          replyCommentId: 0
                          isNotRichText: 1
                        - userName: zhangchuan2288
                          nickName: 朝夕。
                          source: 0
                          type: 2
                          content: 来骑车
                          createTime: 1690617438
                          commentId: 33
                          replyCommentId: 1
                          isNotRichText: 1
                        - userName: wxid_o2m8xm71c23522
                          nickName: Sunny girl🌼
                          source: 0
                          type: 2
                          content: 啥时候回来的 请我吃饭
                          createTime: 1690617670
                          commentId: 67
                          replyCommentId: 0
                          isNotRichText: 1
                        - userName: wxid_98pjjzpiisi721
                          nickName: 宋端雅
                          source: 0
                          type: 2
                          content: 悠着点，别被吹跑了
                          createTime: 1690617913
                          commentId: 97
                          replyCommentId: 0
                          isNotRichText: 1
                        - userName: zhangchuan2288
                          nickName: 朝夕。
                          source: 0
                          type: 2
                          content: 眼见着雨下来，没跑掉[苦涩][苦涩]
                          createTime: 1690618623
                          commentId: 129
                          replyCommentId: 97
                          isNotRichText: 1
                        - userName: zhangchuan2288
                          nickName: 朝夕。
                          source: 0
                          type: 2
                          content: 等我攒攒钱的
                          createTime: 1690618651
                          commentId: 161
                          replyCommentId: 67
                          isNotRichText: 1
                        - userName: wxid_5hafab2a85yk12
                          nickName: 丶zoū zoú zoǔ zoù 👾
                          source: 0
                          type: 2
                          content: 好一波互相拉扯
                          createTime: 1690621406
                          commentId: 193
                          replyCommentId: 0
                          isNotRichText: 1
                        - userName: zhangchuan2288
                          nickName: 朝夕。
                          source: 0
                          type: 2
                          content: 找你老铁来骑车
                          createTime: 1690623263
                          commentId: 225
                          replyCommentId: 193
                          isNotRichText: 1
                        - userName: wxid_krcc8ziwchbj22
                          nickName: 李顺利
                          source: 13
                          type: 2
                          content: 来喝酒
                          createTime: 1690623942
                          commentId: 259
                          replyCommentId: 1
                          isNotRichText: 1
                        - userName: wxid_jcllrz90yht022
                          nickName: ^^辻弌^^
                          source: 0
                          type: 2
                          content: 又换车了
                          createTime: 1690627357
                          commentId: 289
                          replyCommentId: 0
                          isNotRichText: 1
                        - userName: zhangchuan2288
                          nickName: 朝夕。
                          source: 0
                          type: 2
                          content: 换个绿色经济的[破涕为笑]
                          createTime: 1690627739
                          commentId: 321
                          replyCommentId: 289
                          isNotRichText: 1
                        - userName: wxid_jcllrz90yht022
                          nickName: ^^辻弌^^
                          source: 0
                          type: 2
                          content: 我更绿色  都步行现在[旺柴]
                          createTime: 1690627988
                          commentId: 353
                          replyCommentId: 321
                          isNotRichText: 1
                        - userName: zhangchuan2288
                          nickName: 朝夕。
                          source: 0
                          type: 2
                          content: 步行速度上不来
                          createTime: 1690628270
                          commentId: 385
                          replyCommentId: 353
                          isNotRichText: 1
                        - userName: wxid_5hafab2a85yk12
                          nickName: 丶zoū zoú zoǔ zoù 👾
                          source: 0
                          type: 2
                          content: 今年不参加任何体力活动
                          createTime: 1690628921
                          commentId: 417
                          replyCommentId: 225
                          isNotRichText: 1
                      withUserCount: 0
                      withUserList: null
                    - id: 14176439663782334000
                      userName: zhangchuan2288
                      nickName: 朝夕。
                      createTime: 1689963300
                      snsXml: >-
                        <TimelineObject><id>14176439663782335026</id><username>zhangchuan2288</username><createTime>1689963300</createTime><contentDesc>你见过凌晨两点大雨滂沱后的丰县吗</contentDesc><contentDescShowType>0</contentDescShowType><contentDescScene>3</contentDescScene><private>0</private><sightFolded>0</sightFolded><showFlag>0</showFlag><appInfo><id></id><version></version><appName></appName><installUrl></installUrl><fromUrl></fromUrl><isForceUpdate>0</isForceUpdate><isHidden>0</isHidden></appInfo><sourceUserName></sourceUserName><sourceNickName></sourceNickName><statisticsData></statisticsData><statExtStr></statExtStr><ContentObject><contentStyle>1</contentStyle><title></title><description></description><mediaList><media><id>14176439664776254003</id><type>2</type><title></title><description>你见过凌晨两点大雨滂沱后的丰县吗</description><private>0</private><userData></userData><subType>0</subType><videoSize
                        width="4032" height="3024"></videoSize><url type="1"
                        md5="36dbd565064958035f6588c2fb6f291f"
                        videomd5="">http://shmmsns.qpic.cn/mmsns/FzeKA69P5uIdqPfQxp59LoJ5ysYwVnqfMlFNANT7K8R7Ze1rdaS70CnNlpKJjLI5dIibqM0qdO8k/0</url><thumb
                        type="1">http://shmmsns.qpic.cn/mmsns/FzeKA69P5uIdqPfQxp59LoJ5ysYwVnqfMlFNANT7K8R7Ze1rdaS70CnNlpKJjLI5dIibqM0qdO8k/150</thumb><size
                        width="1080.000000" height="1440.000000"
                        totalSize="35585"></size></media><media><id>14176439664787001918</id><type>2</type><title></title><description></description><private>0</private><userData></userData><subType>0</subType><videoSize
                        width="4032" height="3024"></videoSize><url type="1"
                        md5="bd04b764e56258df05eaf7bb5b573b71"
                        videomd5="">http://shmmsns.qpic.cn/mmsns/FzeKA69P5uIdqPfQxp59LoJ5ysYwVnqf4HCrN2pRyfMsYbCEFPibhhJxuhqLKm6gGibZJ1O8dCjFk/0</url><thumb
                        type="1">http://shmmsns.qpic.cn/mmsns/FzeKA69P5uIdqPfQxp59LoJ5ysYwVnqf4HCrN2pRyfMsYbCEFPibhhJxuhqLKm6gGibZJ1O8dCjFk/150</thumb><size
                        width="1080.000000" height="1440.000000"
                        totalSize="98413"></size></media><media><id>14176439664799781442</id><type>2</type><title></title><description></description><private>0</private><userData></userData><subType>0</subType><videoSize
                        width="4032" height="3024"></videoSize><url type="1"
                        md5="aff12615ed1162e9e489180e7ae16202"
                        videomd5="">http://shmmsns.qpic.cn/mmsns/FzeKA69P5uIdqPfQxp59Lia2vWzK79RWPM1icwp4QNQ5JriaibFpOd8ryfRQMaCs3owfpdOjSZzfoeI/0</url><thumb
                        type="1">http://shmmsns.qpic.cn/mmsns/FzeKA69P5uIdqPfQxp59Lia2vWzK79RWPM1icwp4QNQ5JriaibFpOd8ryfRQMaCs3owfpdOjSZzfoeI/150</thumb><size
                        width="1440.000000" height="1080.000000"
                        totalSize="146584"></size></media></mediaList><contentUrl></contentUrl></ContentObject><actionInfo><appMsg><messageAction></messageAction></appMsg></actionInfo><location
                        poiClassifyId="" poiName="" poiAddress=""
                        poiClassifyType="0"
                        city=""></location><publicUserName></publicUserName><streamvideo><streamvideourl></streamvideourl><streamvideothumburl></streamvideothumburl><streamvideoweburl></streamvideoweburl></streamvideo></TimelineObject>
                      likeCount: 5
                      likeList:
                        - userName: wxid_i6qsbbjenjuj22
                          nickName: Mr李
                          source: 0
                          type: 1
                          createTime: 1689964711
                        - userName: wxid_v5z9pqicwzlv22
                          nickName: 小轩电玩-Gt
                          source: 0
                          type: 1
                          createTime: 1689966969
                        - userName: wxid_jcllrz90yht022
                          nickName: ^^辻弌^^
                          source: 0
                          type: 1
                          createTime: 1689974931
                        - userName: wxid_3tctjyoc91u322
                          nickName: 大乞丐
                          source: 0
                          type: 1
                          createTime: 1689978807
                        - userName: wxid_98pjjzpiisi721
                          nickName: 宋端雅
                          source: 0
                          type: 1
                          createTime: 1689983376
                      commentCount: 1
                      commentList:
                        - userName: wxid_0rp825czl4o722
                          nickName: 小小晴仔🐳
                          source: 0
                          type: 2
                          content: 没回市里吗
                          createTime: 1689986721
                          commentId: 1
                          replyCommentId: 0
                          isNotRichText: 1
                      withUserCount: 0
                      withUserList: null
                    - id: 14176296271561167000
                      userName: zhangchuan2288
                      nickName: 朝夕。
                      createTime: 1689946207
                      snsXml: >-
                        <TimelineObject><id>14176296271561167412</id><username>zhangchuan2288</username><createTime>1689946207</createTime><contentDesc>123123</contentDesc><contentDescShowType>0</contentDescShowType><contentDescScene>3</contentDescScene><private>0</private><sightFolded>0</sightFolded><showFlag>0</showFlag><appInfo><id></id><version></version><appName></appName><installUrl></installUrl><fromUrl></fromUrl><isForceUpdate>0</isForceUpdate><isHidden>0</isHidden></appInfo><sourceUserName></sourceUserName><sourceNickName></sourceNickName><statisticsData></statisticsData><statExtStr></statExtStr><ContentObject><contentStyle>1</contentStyle><title></title><description></description><mediaList><media><id>14176296272322302512</id><type>2</type><title></title><description>123123</description><private>0</private><userData></userData><subType>0</subType><videoSize
                        width="1080" height="1920"></videoSize><url type="1"
                        md5="6b13c29800d654720c20d06be182bab4"
                        videomd5="">http://shmmsns.qpic.cn/mmsns/FzeKA69P5uIdqPfQxp59LiaMSyibI7Aib340YxQPo8uF7prNoz2X3ca6DDQVdETpBJuKZbwMytfenA/0</url><thumb
                        type="1">http://shmmsns.qpic.cn/mmsns/FzeKA69P5uIdqPfQxp59LiaMSyibI7Aib340YxQPo8uF7prNoz2X3ca6DDQVdETpBJuKZbwMytfenA/150</thumb><size
                        width="1080.000000" height="1920.000000"
                        totalSize="39784"></size></media></mediaList><contentUrl></contentUrl></ContentObject><actionInfo><appMsg><messageAction></messageAction></appMsg></actionInfo><location
                        poiClassifyId="" poiName="" poiAddress=""
                        poiClassifyType="0"
                        city=""></location><publicUserName></publicUserName><streamvideo><streamvideourl></streamvideourl><streamvideothumburl></streamvideothumburl><streamvideoweburl></streamvideoweburl></streamvideo></TimelineObject>
                      likeCount: 0
                      likeList: null
                      commentCount: 0
                      commentList: null
                      withUserCount: 0
                      withUserList: null
                    - id: 14053838050949140000
                      userName: zhangchuan2288
                      nickName: 朝夕。
                      createTime: 1675348049
                      snsXml: >-
                        <TimelineObject><id>14053838050949140796</id><username>zhangchuan2288</username><createTime>1675348049</createTime><contentDesc>前几天设置微信标签误操作删除了一群好友，今天才发现，万分抱歉[苦涩][苦涩]</contentDesc><contentDescShowType>0</contentDescShowType><contentDescScene>3</contentDescScene><private>0</private><sightFolded>0</sightFolded><showFlag>0</showFlag><appInfo><id></id><version></version><appName></appName><installUrl></installUrl><fromUrl></fromUrl><isForceUpdate>0</isForceUpdate></appInfo><sourceUserName></sourceUserName><sourceNickName></sourceNickName><statisticsData></statisticsData><statExtStr></statExtStr><ContentObject><contentStyle>1</contentStyle><title></title><description></description><mediaList><media><id>14053838051741077847</id><type>2</type><title></title><description>前几天设置微信标签误操作删除了一群好友，今天才发现，万分抱歉[苦涩][苦涩]</description><private>0</private><userData></userData><subType>0</subType><videoSize
                        width="400" height="400"></videoSize><url type="1"
                        md5="045b93b87537f661a6a519ae20df9d56"
                        videomd5="">http://shmmsns.qpic.cn/mmsns/FzeKA69P5uIdqPfQxp59LoYpyLAbCah3ticTAbp6pdnGV3hSHuc6iaqWwboJ14OgxFPgDuzxYSEIQ/0</url><thumb
                        type="1">http://shmmsns.qpic.cn/mmsns/FzeKA69P5uIdqPfQxp59LoYpyLAbCah3ticTAbp6pdnGV3hSHuc6iaqWwboJ14OgxFPgDuzxYSEIQ/150</thumb><size
                        width="400.000000" height="400.000000"
                        totalSize="5992"></size></media></mediaList><contentUrl></contentUrl></ContentObject><actionInfo><appMsg><messageAction></messageAction></appMsg></actionInfo><location
                        poiClassifyId="" poiName="" poiAddress=""
                        poiClassifyType="0"
                        city=""></location><publicUserName></publicUserName><streamvideo><streamvideourl></streamvideourl><streamvideothumburl></streamvideothumburl><streamvideoweburl></streamvideoweburl></streamvideo></TimelineObject>
                      likeCount: 1
                      likeList:
                        - userName: wxid_j12g1qxcbfrs22
                          nickName: 国杠1573
                          source: 0
                          type: 1
                          createTime: 1675402283
                      commentCount: 1
                      commentList:
                        - userName: zhangchuan2288
                          nickName: 朝夕。
                          source: 0
                          type: 2
                          content: 已经加回来一批了，还漏哪些也不知道了。有共同好友提到这个事情还请帮忙转发个名片[抱拳][抱拳]
                          createTime: 1675348474
                          commentId: 1
                          replyCommentId: 0
                          isNotRichText: 1
                      withUserCount: 0
                      withUserList: null
                    - id: 14049821398518206000
                      userName: zhangchuan2288
                      nickName: 朝夕。
                      createTime: 1674869227
                      snsXml: >-
                        <TimelineObject><id>14049821398518206772</id><username>zhangchuan2288</username><createTime>1674869227</createTime><contentDesc>婚礼圆满结束，感谢各位亲朋好友前来捧场，招待不周的地方还请包涵。</contentDesc><contentDescShowType>0</contentDescShowType><contentDescScene>4</contentDescScene><private>0</private><sightFolded>0</sightFolded><showFlag>0</showFlag><appInfo><id>wxa5e0de08d96cc09d</id><version>47</version><appName>秒剪</appName><installUrl></installUrl><fromUrl></fromUrl><isForceUpdate>0</isForceUpdate><clickable>0</clickable></appInfo><sourceUserName></sourceUserName><sourceNickName></sourceNickName><statisticsData></statisticsData><actionInfo><appMsg><appid>wxa5e0de08d96cc09d</appid><mediaTagName></mediaTagName><messageExt><![CDATA[{
                          &quot;page&quot; : &quot;1&quot;,
                          &quot;miaojianExtInfo&quot; : &quot;eyJtdXNpY0tleSI6IjA6MzEyMjM2MTc5OjEiLCJ0ZW1wbGF0ZUlkIjoiWl85XzE2X3d1bW9iYW4iLCJ2aWRlb1NvdXJjZVR5cGUiOjAsImNyZWF0aW9uSWQiOiIzREQzQzg4NC02ODI2LTRBNUItQUIwMy02NEM5Mjk3RjIxOTgiLCJwbGF5bGlzdElkIjowLCJ2aWRlb0ZpbGVNRDUiOiI1MDk2YTA3N2E1NjA5YWFlMjcyNWQyODFiNWFhMGM3YyIsInJhdGlvVHlwZSI6IjlfMTYiLCJwYWdlIjoiMSIsInNhdmVUaW1lIjoxNjc0ODY5MTMwMjA5LCJwcm9qZWN0SWQiOiJBODM2MzQxOC1CMjc1LTRDQTMtQTMwQi05QjdFQ0E4MDdDRDEtMTY3NDg2ODA1NSJ9&quot;,
                          &quot;displayName&quot; : &quot;用秒剪做视频&quot;
                        }]]></messageExt><messageAction><![CDATA[(null)]]></messageAction></appMsg><scene>0</scene><type>0</type><url></url><newWordingKey></newWordingKey><newtype>0</newtype><installedWording></installedWording><uninstalledWording></uninstalledWording></actionInfo><statExtStr>GhQKEnd4YTVlMGRlMDhkOTZjYzA5ZA==</statExtStr><ContentObject><contentStyle>15</contentStyle><title>微信小视频</title><description>秒剪</description><mediaList><media><id>14049821398988099892</id><type>6</type><title></title><description>婚礼圆满结束，感谢各位亲朋好友前来捧场，招待不周的地方还请包涵。</description><private>0</private><userData></userData><subType>0</subType><videoSize
                        width="0" height="0"></videoSize><url type="1"
                        md5="fa2936beca76684700a54aa2cc31fd14"
                        videomd5="5096a077a5609aae2725d281b5aa0c7c">http://shzjwxsns.video.qq.com/102/20202/snsvideodownload?filekey=30350201010421301f020166040253480410fa2936beca76684700a54aa2cc31fd14020400cc1d82040d00000004627466730000000132&amp;hy=SH&amp;storeid=563d479ea00013d128399cc840000006600004eea53480288bb01e6cbc6fd8&amp;dotrans=10&amp;ef=30_0&amp;bizid=1023&amp;dur=10</url><thumb
                        type="1">http://vweixinthumb.tc.qq.com/150/20250/snsvideodownload?filekey=30340201010420301e020200960402534804108f1d982e76083ec8f9381dad1d24543702020a71040d00000004627466730000000132&amp;hy=SH&amp;storeid=563d479e9000c0c368399cc840000009600004f1a5348228e7b01e6a8f348a&amp;bizid=1023</thumb><size
                        width="224.000000" height="398.000000"
                        totalSize="13376898"></size><videoDuration>10.346000</videoDuration><VideoColdDLRule><All>CAISBAgWEAEoAjAc</All></VideoColdDLRule></media></mediaList><contentUrl>https://support.weixin.qq.com/cgi-bin/mmsupport-bin/readtemplate?t=page/common_page__upgrade&amp;v=1</contentUrl></ContentObject><location
                        poiClassifyId="" poiName="" poiAddress=""
                        poiClassifyType="0"
                        city=""></location><publicUserName></publicUserName><streamvideo><streamvideourl></streamvideourl><streamvideothumburl></streamvideothumburl><streamvideoweburl></streamvideoweburl></streamvideo></TimelineObject>
                      likeCount: 27
                      likeList:
                        - userName: wxid_9728427285512
                          nickName: 蘇苏
                          source: 0
                          type: 1
                          createTime: 1674869459
                        - userName: wxid_39uo3afe9rzj22
                          nickName: Z
                          source: 0
                          type: 1
                          createTime: 1674869468
                        - userName: wxid_fjbpmkegghbm21
                          nickName: 山山而川
                          source: 0
                          type: 1
                          createTime: 1674869528
                        - userName: wxid_bwtz9nn9yds422
                          nickName: 大鸭梨
                          source: 0
                          type: 1
                          createTime: 1674869683
                        - userName: wxid_ehcl9lv7l8rs22
                          nickName: X-zzzz
                          source: 0
                          type: 1
                          createTime: 1674869789
                        - userName: wxid_98pjjzpiisi721
                          nickName: 宋端雅
                          source: 0
                          type: 1
                          createTime: 1674869865
                        - userName: wxid_5101821019212
                          nickName: 聪聪
                          source: 0
                          type: 1
                          createTime: 1674870043
                        - userName: wxid_p0gqihfs2p5q22
                          nickName: 优红酒业首席侍酒师：马明明
                          source: 0
                          type: 1
                          createTime: 1674870199
                        - userName: L976863774
                          nickName: 清风揽月阁คิดถึง
                          source: 0
                          type: 1
                          createTime: 1674870491
                        - userName: wxid_i6qsbbjenjuj22
                          nickName: Mr李
                          source: 0
                          type: 1
                          createTime: 1674870606
                        - userName: qq-wuboxiao
                          nickName: 🐝。
                          source: 0
                          type: 1
                          createTime: 1674870643
                        - userName: wxid_5hafab2a85yk12
                          nickName: 丶zoū zoú zoǔ zoù 👾
                          source: 0
                          type: 1
                          createTime: 1674870747
                        - userName: wxid_6xi2yuy30id422
                          nickName: 。
                          source: 0
                          type: 1
                          createTime: 1674871041
                        - userName: wxid_fksqykd1a16321
                          nickName: 海蓝蓝的！
                          source: 0
                          type: 1
                          createTime: 1674871101
                        - userName: wxid_pw89aeo8dbu621
                          nickName: 恰巧经过。
                          source: 0
                          type: 1
                          createTime: 1674871465
                        - userName: wxid_3896338963812
                          nickName: 刁民
                          source: 0
                          type: 1
                          createTime: 1674871554
                        - userName: wxid_0rp825czl4o722
                          nickName: 小小晴仔🐳
                          source: 0
                          type: 1
                          createTime: 1674871561
                        - userName: wxid_jvps04ejr41q22
                          nickName: 爱吃🐟的猫
                          source: 0
                          type: 1
                          createTime: 1674871584
                        - userName: wxid_j12g1qxcbfrs22
                          nickName: 国杠1573
                          source: 0
                          type: 1
                          createTime: 1674871777
                        - userName: wxid_306am6wo0bug21
                          nickName: JUST DO IT
                          source: 0
                          type: 1
                          createTime: 1674871830
                        - userName: wxid_5etgnoe0q7ih22
                          nickName: 姚硕
                          source: 0
                          type: 1
                          createTime: 1674872429
                        - userName: wxid_dgd90bbsgep21
                          nickName:  思念
                          source: 0
                          type: 1
                          createTime: 1674872530
                        - userName: wxid_jcllrz90yht022
                          nickName: ^^辻弌^^
                          source: 0
                          type: 1
                          createTime: 1674873099
                        - userName: wxid_cy6buf12nf6921
                          nickName: 暖心
                          source: 0
                          type: 1
                          createTime: 1674878049
                        - userName: wxid_wc8vxsnwjew522
                          nickName: star.💫
                          source: 0
                          type: 1
                          createTime: 1674881445
                        - userName: star911128
                          nickName: 咩咩咪丫-休假中，有事电联
                          source: 0
                          type: 1
                          createTime: 1674886673
                        - userName: wxid_nwp0zo36a0xo52
                          nickName: ^_^💗🐎
                          source: 0
                          type: 1
                          createTime: 1674954994
                      commentCount: 3
                      commentList:
                        - userName: wxid_fjbpmkegghbm21
                          nickName: 山山而川
                          source: 0
                          type: 2
                          content: 恭喜恭喜
                          createTime: 1674869547
                          commentId: 1
                          replyCommentId: 0
                          isNotRichText: 1
                        - userName: wxid_bwtz9nn9yds422
                          nickName: 大鸭梨
                          source: 0
                          type: 2
                          content: 祝99
                          createTime: 1674869699
                          commentId: 33
                          replyCommentId: 0
                          isNotRichText: 1
                        - userName: wxid_39uo3afe9rzj22
                          nickName: Z
                          source: 0
                          type: 2
                          content: 恭喜恭喜，百年好合，早生贵子[愉快]
                          createTime: 1674869818
                          commentId: 67
                          replyCommentId: 0
                          isNotRichText: 1
                      withUserCount: 0
                      withUserList: null
                    - id: 14032731132213137000
                      userName: zhangchuan2288
                      nickName: 朝夕。
                      createTime: 1672831908
                      snsXml: >-
                        <TimelineObject><id>14032731132213137733</id><username>zhangchuan2288</username><createTime>1672831908</createTime><contentDesc>份子钱都准备一下[吃瓜][吃瓜]</contentDesc><contentDescShowType>0</contentDescShowType><contentDescScene>4</contentDescScene><private>0</private><sightFolded>0</sightFolded><showFlag>0</showFlag><appInfo><id></id><version></version><appName></appName><installUrl></installUrl><fromUrl></fromUrl><isForceUpdate>0</isForceUpdate></appInfo><sourceUserName></sourceUserName><sourceNickName></sourceNickName><statisticsData></statisticsData><statExtStr>GhQKEnd4ZjI3MjcwNjg2NDUxODYzMw==</statExtStr><ContentObject><contentStyle>3</contentStyle><title>有幸与你相爱❤️</title><description></description><contentUrl>https://h5.hunbei5.com/app/A1311g44svSlw?state=&amp;f_user=70200112</contentUrl><mediaList><media><id>14032731132610744623</id><type>2</type><title></title><description></description><private>0</private><userData></userData><subType>0</subType><videoSize
                        width="0" height="0"></videoSize><url type="0" md5=""
                        videomd5="">https://h5cdn.hunbei1.com/upload/scene/8029272/2047587de022e74841b6ed2ae92646daf5219ec.png?imageMogr2/thumbnail/255x255</url><lowBandUrl
                        type="0">https://h5cdn.hunbei1.com/upload/scene/8029272/2047587de022e74841b6ed2ae92646daf5219ec.png?imageMogr2/thumbnail/255x255</lowBandUrl><thumb
                        type="1">http://shmmsns.qpic.cn/mmsns/FzeKA69P5uIdqPfQxp59Lutdvynf2xjHz5Jq1bTtOlla8AODTtyU7caFcdIt0LW3bOr0ibUDQrOY/150</thumb></media></mediaList></ContentObject><actionInfo><appMsg><messageAction></messageAction></appMsg></actionInfo><location
                        poiClassifyId="" poiName="" poiAddress=""
                        poiClassifyType="0"
                        city=""></location><publicUserName></publicUserName><streamvideo><streamvideourl></streamvideourl><streamvideothumburl></streamvideothumburl><streamvideoweburl></streamvideoweburl></streamvideo></TimelineObject>
                      likeCount: 17
                      likeList:
                        - userName: zhangchuan2288
                          nickName: 朝夕。
                          source: 0
                          type: 1
                          createTime: 1672832037
                        - userName: wxid_cy6buf12nf6921
                          nickName: 暖心
                          source: 0
                          type: 1
                          createTime: 1672832425
                        - userName: wxid_i6qsbbjenjuj22
                          nickName: Mr李
                          source: 0
                          type: 1
                          createTime: 1672832471
                        - userName: wxid_zekmthb36vox21
                          nickName: 小灰灰🍃
                          source: 0
                          type: 1
                          createTime: 1672832723
                        - userName: wxid_ehcl9lv7l8rs22
                          nickName: X-zzzz
                          source: 0
                          type: 1
                          createTime: 1672832774
                        - userName: wxid_0rp825czl4o722
                          nickName: 小小晴仔🐳
                          source: 0
                          type: 1
                          createTime: 1672832833
                        - userName: wxid_arr2oudb8in722
                          nickName: 邢洪阳
                          source: 0
                          type: 1
                          createTime: 1672832904
                        - userName: wxid_j12g1qxcbfrs22
                          nickName: 国杠1573
                          source: 0
                          type: 1
                          createTime: 1672833135
                        - userName: wxid_5101821019212
                          nickName: 聪聪
                          source: 0
                          type: 1
                          createTime: 1672833999
                        - userName: wxid_91eswkq1be2542
                          nickName: 网事如烟
                          source: 0
                          type: 1
                          createTime: 1672834527
                        - userName: wxid_l2k8g89qcuio22
                          nickName: 🌻  sun flower
                          source: 0
                          type: 1
                          createTime: 1672835417
                        - userName: wxid_5hafab2a85yk12
                          nickName: 丶zoū zoú zoǔ zoù 👾
                          source: 0
                          type: 1
                          createTime: 1672835534
                        - userName: wxid_6juk7pnvjg2s22
                          nickName: 丫头
                          source: 0
                          type: 1
                          createTime: 1672836185
                        - userName: wxid_9728427285512
                          nickName: 蘇苏
                          source: 0
                          type: 1
                          createTime: 1672836260
                        - userName: wxid_hmj7c4ugns8e21
                          nickName: 张
                          source: 0
                          type: 1
                          createTime: 1672841988
                        - userName: wxid_6xi2yuy30id422
                          nickName: 。
                          source: 0
                          type: 1
                          createTime: 1672842266
                        - userName: wxid_0k0ypmlvqvq222
                          nickName: 后面还有我
                          source: 0
                          type: 1
                          createTime: 1672905232
                      commentCount: 21
                      commentList:
                        - userName: wxid_5101821019212
                          nickName: 聪聪
                          source: 0
                          type: 2
                          content: 改时间了？
                          createTime: 1672834021
                          commentId: 1
                          replyCommentId: 0
                          isNotRichText: 1
                        - userName: zhangchuan2288
                          nickName: 朝夕。
                          source: 0
                          type: 2
                          content: 昂，改成初六了
                          createTime: 1672834048
                          commentId: 33
                          replyCommentId: 1
                          isNotRichText: 1
                        - userName: wxid_5101821019212
                          nickName: 聪聪
                          source: 0
                          type: 2
                          content: 也好  初六人多点热闹
                          createTime: 1672834315
                          commentId: 65
                          replyCommentId: 33
                          isNotRichText: 1
                        - userName: zhangchuan2288
                          nickName: 朝夕。
                          source: 0
                          type: 2
                          content: 嗯嗯[笑脸]
                          createTime: 1672834347
                          commentId: 97
                          replyCommentId: 65
                          isNotRichText: 1
                        - userName: wxid_98pjjzpiisi721
                          nickName: 宋端雅
                          source: 0
                          type: 2
                          content: '[红包][红包][红包]'
                          createTime: 1672834487
                          commentId: 129
                          replyCommentId: 0
                          isNotRichText: 1
                        - userName: wxid_pw89aeo8dbu621
                          nickName: 恰巧经过。
                          source: 0
                          type: 2
                          content: 先互删一个月吧
                          createTime: 1672835409
                          commentId: 161
                          replyCommentId: 0
                          isNotRichText: 1
                        - userName: zhangchuan2288
                          nickName: 朝夕。
                          source: 0
                          type: 2
                          content: 还指望你当伴郎的，你要不来把腿给你打断
                          createTime: 1672835471
                          commentId: 193
                          replyCommentId: 161
                          isNotRichText: 1
                        - userName: wxid_5hafab2a85yk12
                          nickName: 丶zoū zoú zoǔ zoù 👾
                          source: 0
                          type: 2
                          content: 打断腿太残忍了！婚车走他家门口！
                          createTime: 1672835587
                          commentId: 225
                          replyCommentId: 193
                          isNotRichText: 1
                        - userName: zhangchuan2288
                          nickName: 朝夕。
                          source: 0
                          type: 2
                          content: 也行，在他家门口停一会
                          createTime: 1672835641
                          commentId: 257
                          replyCommentId: 225
                          isNotRichText: 1
                        - userName: wxid_5hafab2a85yk12
                          nickName: 丶zoū zoú zoǔ zoù 👾
                          source: 0
                          type: 2
                          content: 虾仁要配猪心
                          createTime: 1672835769
                          commentId: 289
                          replyCommentId: 257
                          isNotRichText: 1
                        - userName: wxid_pw89aeo8dbu621
                          nickName: 恰巧经过。
                          source: 0
                          type: 2
                          content: 你麻溜的滚
                          createTime: 1672836371
                          commentId: 321
                          replyCommentId: 225
                          isNotRichText: 1
                        - userName: wxid_i6qsbbjenjuj22
                          nickName: Mr李
                          source: 0
                          type: 2
                          content: 衬托颜值？
                          createTime: 1672838373
                          commentId: 353
                          replyCommentId: 193
                          isNotRichText: 1
                        - userName: zhangchuan2288
                          nickName: 朝夕。
                          source: 0
                          type: 2
                          content: 有这方面考量，主要衬托身材
                          createTime: 1672838519
                          commentId: 385
                          replyCommentId: 353
                          isNotRichText: 1
                        - userName: wxid_sahb2j8lj3tr22
                          nickName: 菠萝蜜
                          source: 0
                          type: 2
                          content: 恭喜恭喜，祝我表弟永结同心[庆祝][庆祝][庆祝]
                          createTime: 1672839103
                          commentId: 419
                          replyCommentId: 0
                          isNotRichText: 1
                        - userName: zhangchuan2288
                          nickName: 朝夕。
                          source: 0
                          type: 2
                          content: 谢谢我大表姐[破涕为笑]
                          createTime: 1672839138
                          commentId: 449
                          replyCommentId: 419
                          isNotRichText: 1
                        - userName: wxid_a3lf3pj8uy7i21
                          nickName: ꪶäꪗღꪖꪸꪀ俗人
                          source: 0
                          type: 2
                          content: 突如其来的结果请柬，我得连夜借钱[捂脸]
                          createTime: 1672874592
                          commentId: 481
                          replyCommentId: 0
                          isNotRichText: 1
                        - userName: zhangchuan2288
                          nickName: 朝夕。
                          source: 0
                          type: 2
                          content: '[破涕为笑][破涕为笑]'
                          createTime: 1672884385
                          commentId: 513
                          replyCommentId: 481
                          isNotRichText: 1
                        - userName: wxid_a3lf3pj8uy7i21
                          nickName: ꪶäꪗღꪖꪸꪀ俗人
                          source: 0
                          type: 2
                          content: 吃个大席真难
                          createTime: 1672889889
                          commentId: 545
                          replyCommentId: 513
                          isNotRichText: 1
                        - userName: wxid_a3lf3pj8uy7i21
                          nickName: ꪶäꪗღꪖꪸꪀ俗人
                          source: 0
                          type: 2
                          content: 能打条不[偷笑]
                          createTime: 1672890121
                          commentId: 577
                          replyCommentId: 0
                          isNotRichText: 1
                        - userName: zhangchuan2288
                          nickName: 朝夕。
                          source: 0
                          type: 2
                          content: 管，等你结婚的时候我再把条给你
                          createTime: 1672890199
                          commentId: 609
                          replyCommentId: 577
                          isNotRichText: 1
                        - userName: wxid_a3lf3pj8uy7i21
                          nickName: ꪶäꪗღꪖꪸꪀ俗人
                          source: 0
                          type: 2
                          content: 我看行，
                          createTime: 1672890219
                          commentId: 641
                          replyCommentId: 609
                          isNotRichText: 1
                      withUserCount: 0
                      withUserList: null
                    - id: 14028842879472112000
                      userName: zhangchuan2288
                      nickName: 朝夕。
                      createTime: 1672368392
                      snsXml: >-
                        <TimelineObject><id>14028842879472111958</id><username>zhangchuan2288</username><createTime>1672368392</createTime><contentDesc>官方指定唯一合作伙伴</contentDesc><contentDescShowType>0</contentDescShowType><contentDescScene>3</contentDescScene><private>0</private><sightFolded>0</sightFolded><showFlag>0</showFlag><location
                        city="徐州市" longitude="117.458256" latitude="34.448422"
                        poiName="徐州市 · 徐州市贾汪区民政局" poiAddress="滨河路"
                        poiScale="11.000000" poiInfoUrl=""
                        poiClassifyId="qqmap_7919508333704683966"
                        poiClassifyType="1" poiClickableStatus="0"
                        poiAddressName="徐州市贾汪区民政局"
                        country="中国"></location><appInfo><id></id><version></version><appName></appName><installUrl></installUrl><fromUrl></fromUrl><isForceUpdate>0</isForceUpdate></appInfo><sourceUserName></sourceUserName><sourceNickName></sourceNickName><statisticsData></statisticsData><statExtStr></statExtStr><ContentObject><contentStyle>1</contentStyle><title></title><description></description><mediaList><media><id>14028842879994171721</id><type>2</type><title></title><description>官方指定唯一合作伙伴</description><private>0</private><userData></userData><subType>0</subType><videoSize
                        width="1935" height="1278"></videoSize><url type="1"
                        md5="edddd89eae120dfd9da62afda5b412d8"
                        videomd5="">http://shmmsns.qpic.cn/mmsns/FzeKA69P5uJHUK8kjS3IdV0PWv2fZdgQdiaMYrL8x3kjH5DwtE6dibm89Yru7eYhvmamkpHvGW3bU/0</url><thumb
                        type="1">http://shmmsns.qpic.cn/mmsns/FzeKA69P5uJHUK8kjS3IdV0PWv2fZdgQdiaMYrL8x3kjH5DwtE6dibm89Yru7eYhvmamkpHvGW3bU/150</thumb><size
                        width="1729.000000" height="1080.000000"
                        totalSize="130285"></size></media><media><id>14028842879992992048</id><type>2</type><title></title><description></description><private>0</private><userData></userData><subType>0</subType><videoSize
                        width="1280" height="1707"></videoSize><url type="1"
                        md5="999b5b33dc13ec36df33b8981dae19fd"
                        videomd5="">http://shmmsns.qpic.cn/mmsns/FzeKA69P5uJHUK8kjS3IdV0PWv2fZdgQqE9FgTx0urSTg6OEVpxlP7KjE40OZpvZ0c5RkQueq5c/0</url><thumb
                        type="1">http://shmmsns.qpic.cn/mmsns/FzeKA69P5uJHUK8kjS3IdV0PWv2fZdgQqE9FgTx0urSTg6OEVpxlP7KjE40OZpvZ0c5RkQueq5c/150</thumb><size
                        width="1080.000000" height="1440.000000"
                        totalSize="146797"></size></media><media><id>14028842879999480152</id><type>2</type><title></title><description></description><private>0</private><userData></userData><subType>0</subType><videoSize
                        width="1280" height="1707"></videoSize><url type="1"
                        md5="00c045fbd7fe85941f51eff17afc0891"
                        videomd5="">http://shmmsns.qpic.cn/mmsns/FzeKA69P5uJHUK8kjS3IdV0PWv2fZdgQIJS2wdhhGJ2HibMRMWtE6COibthxtSqEh1rJneMca3qSU/0</url><thumb
                        type="1">http://shmmsns.qpic.cn/mmsns/FzeKA69P5uJHUK8kjS3IdV0PWv2fZdgQIJS2wdhhGJ2HibMRMWtE6COibthxtSqEh1rJneMca3qSU/150</thumb><size
                        width="1080.000000" height="1440.000000"
                        totalSize="120531"></size></media><media><id>14028842880002822462</id><type>2</type><title></title><description></description><private>0</private><userData></userData><subType>0</subType><videoSize
                        width="1280" height="1707"></videoSize><url type="1"
                        md5="ac917cdf2623226edf5778633e8a41b3"
                        videomd5="">http://shmmsns.qpic.cn/mmsns/FzeKA69P5uJHUK8kjS3IdV0PWv2fZdgQ0lqjO76AYDtuoGSoN7uWMxa1ZzicbnxqDmFsNbB5Vjuo/0</url><thumb
                        type="1">http://shmmsns.qpic.cn/mmsns/FzeKA69P5uJHUK8kjS3IdV0PWv2fZdgQ0lqjO76AYDtuoGSoN7uWMxa1ZzicbnxqDmFsNbB5Vjuo/150</thumb><size
                        width="1080.000000" height="1440.000000"
                        totalSize="151982"></size></media></mediaList><contentUrl></contentUrl></ContentObject><actionInfo><appMsg><messageAction></messageAction></appMsg></actionInfo><publicUserName></publicUserName><streamvideo><streamvideourl></streamvideourl><streamvideothumburl></streamvideothumburl><streamvideoweburl></streamvideoweburl></streamvideo></TimelineObject>
                      likeCount: 53
                      likeList:
                        - userName: zhangchuan2288
                          nickName: 朝夕。
                          source: 0
                          type: 1
                          createTime: 1672368397
                        - userName: wxid_ehcl9lv7l8rs22
                          nickName: X-zzzz
                          source: 0
                          type: 1
                          createTime: 1672368443
                        - userName: wxid_i4vkh4gy8kkw22
                          nickName: 123.=.flows in you
                          source: 0
                          type: 1
                          createTime: 1672368493
                        - userName: wxid_l2k8g89qcuio22
                          nickName: 🌻  sun flower
                          source: 0
                          type: 1
                          createTime: 1672368520
                        - userName: wxid_bwtz9nn9yds422
                          nickName: 大鸭梨
                          source: 0
                          type: 1
                          createTime: 1672368555
                        - userName: wxid_02mhs3efnfl922
                          nickName: 薄荷糖
                          source: 0
                          type: 1
                          createTime: 1672368603
                        - userName: wxid_beadgckmpee722
                          nickName: A 长期收房，租房 陈娟18851689916
                          source: 0
                          type: 1
                          createTime: 1672368608
                        - userName: wxid_0rp825czl4o722
                          nickName: 小小晴仔🐳
                          source: 0
                          type: 1
                          createTime: 1672368643
                        - userName: wxid_31jdgeq4r2gw22
                          nickName: Justice Rains!!..awwwww
                          source: 0
                          type: 1
                          createTime: 1672368753
                        - userName: wxid_jfrtt9b7mew522
                          nickName: 张小胖
                          source: 0
                          type: 1
                          createTime: 1672368788
                        - userName: wxid_jvps04ejr41q22
                          nickName: 爱吃🐟的猫
                          source: 0
                          type: 1
                          createTime: 1672368876
                        - userName: wxid_bhf0vdaei64u21
                          nickName: 挽风～
                          source: 0
                          type: 1
                          createTime: 1672368902
                        - userName: wxid_fksqykd1a16321
                          nickName: 海蓝蓝的！
                          source: 0
                          type: 1
                          createTime: 1672369004
                        - userName: wxid_5hafab2a85yk12
                          nickName: 丶zoū zoú zoǔ zoù 👾
                          source: 0
                          type: 1
                          createTime: 1672369039
                        - userName: wxid_3866478839212
                          nickName: 群青
                          source: 0
                          type: 1
                          createTime: 1672369166
                        - userName: zhoujianxiao001
                          nickName: 周建晓
                          source: 0
                          type: 1
                          createTime: 1672369188
                        - userName: wxid_cy6buf12nf6921
                          nickName: 暖心
                          source: 0
                          type: 1
                          createTime: 1672369271
                        - userName: wxid_zekmthb36vox21
                          nickName: 小灰灰🍃
                          source: 0
                          type: 1
                          createTime: 1672369448
                        - userName: wxid_w46utiiq7vnr22
                          nickName: 花嫁喜铺，刘莉，15852395746
                          source: 0
                          type: 1
                          createTime: 1672369461
                        - userName: wxid_ruqfsd3649lm12
                          nickName: 奔跑的子弹
                          source: 0
                          type: 1
                          createTime: 1672369496
                        - userName: CHENX199110
                          nickName: Xavier C
                          source: 0
                          type: 1
                          createTime: 1672369610
                        - userName: wxid_tgbraqxcss3r22
                          nickName: 中钰翡翠天境 顾传凯 17368932350
                          source: 0
                          type: 1
                          createTime: 1672369639
                        - userName: wxid_9728427285512
                          nickName: 蘇苏
                          source: 0
                          type: 1
                          createTime: 1672369672
                        - userName: wxid_aookkrtgrmv522
                          nickName: $
                          source: 0
                          type: 1
                          createTime: 1672369851
                        - userName: wxid_ihhaqc6dki3b22
                          nickName: 永不放弃
                          source: 0
                          type: 1
                          createTime: 1672370014
                        - userName: wxid_nasqrofbjvxa22
                          nickName: 灼
                          source: 0
                          type: 1
                          createTime: 1672370097
                        - userName: wxid_6juk7pnvjg2s22
                          nickName: 丫头
                          source: 0
                          type: 1
                          createTime: 1672370272
                        - userName: wxid_91eswkq1be2542
                          nickName: 网事如烟
                          source: 0
                          type: 1
                          createTime: 1672370319
                        - userName: wxid_93ef9s4n0d5a22
                          nickName: 吕芳
                          source: 0
                          type: 1
                          createTime: 1672370425
                        - userName: wxid_pw89aeo8dbu621
                          nickName: 醉、江湖
                          source: 0
                          type: 1
                          createTime: 1672371152
                        - userName: wxid_2bdxd1309vxh21
                          nickName: .
                          source: 0
                          type: 1
                          createTime: 1672371632
                        - userName: star911128
                          nickName: 咩咩咪丫
                          source: 0
                          type: 1
                          createTime: 1672372026
                        - userName: wxid_arr2oudb8in722
                          nickName: 邢洪阳
                          source: 0
                          type: 1
                          createTime: 1672372084
                        - userName: wxid_thd7lxtbjblp22
                          nickName: 王娇
                          source: 0
                          type: 1
                          createTime: 1672372150
                        - userName: zsz1471790192
                          nickName: 阿九
                          source: 0
                          type: 1
                          createTime: 1672372251
                        - userName: wxid_1dqpdd459ngm22
                          nickName: David•Song
                          source: 0
                          type: 1
                          createTime: 1672373332
                        - userName: wxid_q3xwzt5juadi22
                          nickName: 洒脱
                          source: 0
                          type: 1
                          createTime: 1672374611
                        - userName: wxid_sh2epyst780021
                          nickName: Zw.
                          source: 0
                          type: 1
                          createTime: 1672374777
                        - userName: wxid_jcllrz90yht022
                          nickName: ^^辻弌^^
                          source: 0
                          type: 1
                          createTime: 1672375572
                        - userName: wxid_306am6wo0bug21
                          nickName: JUST DO IT
                          source: 0
                          type: 1
                          createTime: 1672375598
                        - userName: wxid_o0h9mxaxflvs22
                          nickName: 向左向右
                          source: 0
                          type: 1
                          createTime: 1672376006
                        - userName: wxid_24m65rz05jn722
                          nickName: 兮颜
                          source: 0
                          type: 1
                          createTime: 1672378150
                        - userName: wxid_5etgnoe0q7ih22
                          nickName: 姚硕
                          source: 0
                          type: 1
                          createTime: 1672378316
                        - userName: wxid_i6qsbbjenjuj22
                          nickName: Mr李
                          source: 0
                          type: 1
                          createTime: 1672378735
                        - userName: wxid_ir8st4av6rbp21
                          nickName: 江宁辣条丶
                          source: 0
                          type: 1
                          createTime: 1672379277
                        - userName: wxid_j12g1qxcbfrs22
                          nickName: 国杠1573
                          source: 0
                          type: 1
                          createTime: 1672379474
                        - userName: wxid_3o3fb2whu7tx22
                          nickName: 沧海候鸟
                          source: 0
                          type: 1
                          createTime: 1672379882
                        - userName: wy495680816
                          nickName: 九筒
                          source: 0
                          type: 1
                          createTime: 1672380571
                        - userName: wxid_7l1kjlw9mf1322
                          nickName: Echon
                          source: 0
                          type: 1
                          createTime: 1672385802
                        - userName: wxid_5042230422112
                          nickName: A 梦里梦见梦不见的梦
                          source: 0
                          type: 1
                          createTime: 1672386154
                        - userName: wxid_q8wot6seh72p21
                          nickName: 岁月静好
                          source: 0
                          type: 1
                          createTime: 1672396162
                        - userName: wxid_hd0tu39hl2lc22
                          nickName: A～东部战区🇨🇳
                          source: 0
                          type: 1
                          createTime: 1672482329
                        - userName: wxid_07czyloujdfn21
                          nickName: 大许@易通汽修
                          source: 0
                          type: 1
                          createTime: 1672482416
                      commentCount: 35
                      commentList:
                        - userName: wxid_ehcl9lv7l8rs22
                          nickName: X-zzzz
                          source: 0
                          type: 2
                          content: '[庆祝][庆祝]'
                          createTime: 1672368458
                          commentId: 1
                          replyCommentId: 0
                          isNotRichText: 1
                        - userName: wxid_i4vkh4gy8kkw22
                          nickName: 123.=.flows in you
                          source: 0
                          type: 2
                          content: 嗨起来
                          createTime: 1672368556
                          commentId: 35
                          replyCommentId: 0
                          isNotRichText: 1
                        - userName: wxid_beadgckmpee722
                          nickName: A 长期收房，租房 陈娟18851689916
                          source: 0
                          type: 2
                          content: 恭喜！恭喜！
                          createTime: 1672368621
                          commentId: 67
                          replyCommentId: 0
                          isNotRichText: 1
                        - userName: wxid_02mhs3efnfl922
                          nickName: 薄荷糖
                          source: 0
                          type: 2
                          content: 恭喜张总[烟花]
                          createTime: 1672368623
                          commentId: 99
                          replyCommentId: 0
                          isNotRichText: 1
                        - userName: zhangchuan2288
                          nickName: 朝夕。
                          source: 0
                          type: 2
                          content: '[笑脸][笑脸]'
                          createTime: 1672368993
                          commentId: 129
                          replyCommentId: 99
                          isNotRichText: 1
                        - userName: zhangchuan2288
                          nickName: 朝夕。
                          source: 0
                          type: 2
                          content: '[笑脸][笑脸]'
                          createTime: 1672369039
                          commentId: 161
                          replyCommentId: 1
                          isNotRichText: 1
                        - userName: wxid_9mh0zy3ydjkg22
                          nickName: 金源五金店13372205081（LY）
                          source: 0
                          type: 2
                          content: '[太阳]'
                          createTime: 1672369475
                          commentId: 193
                          replyCommentId: 0
                          isNotRichText: 1
                        - userName: CHENX199110
                          nickName: Xavier C
                          source: 0
                          type: 2
                          content: 传总新婚快乐
                          createTime: 1672369647
                          commentId: 225
                          replyCommentId: 0
                          isNotRichText: 1
                        - userName: zhangchuan2288
                          nickName: 朝夕。
                          source: 0
                          type: 2
                          content: '[笑脸][笑脸]'
                          createTime: 1672369674
                          commentId: 257
                          replyCommentId: 225
                          isNotRichText: 1
                        - userName: zhangchuan2288
                          nickName: 朝夕。
                          source: 0
                          type: 2
                          content: '[笑脸][笑脸]'
                          createTime: 1672369696
                          commentId: 289
                          replyCommentId: 193
                          isNotRichText: 1
                        - userName: wxid_9728427285512
                          nickName: 蘇苏
                          source: 0
                          type: 2
                          content: 我也是在贾汪领的证
                          createTime: 1672369704
                          commentId: 321
                          replyCommentId: 0
                          isNotRichText: 1
                        - userName: zhangchuan2288
                          nickName: 朝夕。
                          source: 0
                          type: 2
                          content: 下回再去[破涕为笑]
                          createTime: 1672369849
                          commentId: 353
                          replyCommentId: 321
                          isNotRichText: 1
                        - userName: wxid_9728427285512
                          nickName: 蘇苏
                          source: 0
                          type: 2
                          content: 依稀，你还上瘾了？
                          createTime: 1672369922
                          commentId: 385
                          replyCommentId: 353
                          isNotRichText: 1
                        - userName: wxid_l78x0vvt51vm22
                          nickName: A🔴泰州KK张毅涵提前预约
                          source: 0
                          type: 2
                          content: 恭喜🎉恭喜🎉
                          createTime: 1672369988
                          commentId: 419
                          replyCommentId: 0
                          isNotRichText: 1
                        - userName: Yeewei002
                          nickName: yeewei
                          source: 0
                          type: 2
                          content: 郎才女貌[强]
                          createTime: 1672370695
                          commentId: 449
                          replyCommentId: 0
                          isNotRichText: 1
                        - userName: wxid_22qf47httwyg21
                          nickName: 甜着呢🍓
                          source: 0
                          type: 2
                          content: 恭喜恭喜🎉🎊
                          createTime: 1672370940
                          commentId: 481
                          replyCommentId: 0
                          isNotRichText: 1
                        - userName: zhangchuan2288
                          nickName: 朝夕。
                          source: 0
                          type: 2
                          content: '[笑脸][笑脸]'
                          createTime: 1672371035
                          commentId: 513
                          replyCommentId: 449
                          isNotRichText: 1
                        - userName: zhangchuan2288
                          nickName: 朝夕。
                          source: 0
                          type: 2
                          content: '[笑脸][笑脸]'
                          createTime: 1672371042
                          commentId: 545
                          replyCommentId: 419
                          isNotRichText: 1
                        - userName: zhangchuan2288
                          nickName: 朝夕。
                          source: 0
                          type: 2
                          content: '[笑脸][笑脸]'
                          createTime: 1672371048
                          commentId: 577
                          replyCommentId: 481
                          isNotRichText: 1
                        - userName: wxid_v5z9pqicwzlv22
                          nickName: 小轩电玩-Gt
                          source: 0
                          type: 2
                          content: 恭喜
                          createTime: 1672371843
                          commentId: 611
                          replyCommentId: 0
                          isNotRichText: 1
                        - userName: wxid_0k0ypmlvqvq222
                          nickName: 后面还有我
                          source: 0
                          type: 2
                          content: 我反对这门亲事！你配不上人家
                          createTime: 1672372471
                          commentId: 643
                          replyCommentId: 0
                          isNotRichText: 1
                        - userName: zhangchuan2288
                          nickName: 朝夕。
                          source: 0
                          type: 2
                          content: 反对无效
                          createTime: 1672372510
                          commentId: 673
                          replyCommentId: 643
                          isNotRichText: 1
                        - userName: wxid_jcllrz90yht022
                          nickName: ^^辻弌^^
                          source: 0
                          type: 2
                          content: 帅
                          createTime: 1672375578
                          commentId: 705
                          replyCommentId: 0
                          isNotRichText: 1
                        - userName: wxid_306am6wo0bug21
                          nickName: JUST DO IT
                          source: 0
                          type: 2
                          content: 96年，交朋友吗？
                          createTime: 1672375597
                          commentId: 737
                          replyCommentId: 0
                          isNotRichText: 1
                        - userName: zhangchuan2288
                          nickName: 朝夕。
                          source: 0
                          type: 2
                          content: '[笑脸][笑脸]'
                          createTime: 1672376093
                          commentId: 769
                          replyCommentId: 705
                          isNotRichText: 1
                        - userName: wxid_jcllrz90yht022
                          nickName: ^^辻弌^^
                          source: 0
                          type: 2
                          content: '啥时候举办婚礼啊 '
                          createTime: 1672376200
                          commentId: 801
                          replyCommentId: 769
                          isNotRichText: 1
                        - userName: zhangchuan2288
                          nickName: 朝夕。
                          source: 0
                          type: 2
                          content: ？？
                          createTime: 1672376212
                          commentId: 833
                          replyCommentId: 737
                          isNotRichText: 1
                        - userName: zhangchuan2288
                          nickName: 朝夕。
                          source: 0
                          type: 2
                          content: 还没定，过段时间再定
                          createTime: 1672376232
                          commentId: 865
                          replyCommentId: 801
                          isNotRichText: 1
                        - userName: wxid_jcllrz90yht022
                          nickName: ^^辻弌^^
                          source: 0
                          type: 2
                          content: |-
                            这是年前不回来了？ 
                            在家办人生大事啊
                          createTime: 1672376294
                          commentId: 897
                          replyCommentId: 865
                          isNotRichText: 1
                        - userName: zhangchuan2288
                          nickName: 朝夕。
                          source: 0
                          type: 2
                          content: 过几天回去
                          createTime: 1672376366
                          commentId: 929
                          replyCommentId: 897
                          isNotRichText: 1
                        - userName: wxid_jcllrz90yht022
                          nickName: ^^辻弌^^
                          source: 0
                          type: 2
                          content: 回来年前不得喝一顿嘛
                          createTime: 1672376421
                          commentId: 961
                          replyCommentId: 929
                          isNotRichText: 1
                        - userName: zhangchuan2288
                          nickName: 朝夕。
                          source: 0
                          type: 2
                          content: 喝
                          createTime: 1672376567
                          commentId: 993
                          replyCommentId: 961
                          isNotRichText: 1
                        - userName: wy495680816
                          nickName: 九筒
                          source: 0
                          type: 2
                          content: 我话说完了，谁赞成谁反对
                          createTime: 1672380585
                          commentId: 1025
                          replyCommentId: 0
                          isNotRichText: 1
                        - userName: zhangchuan2288
                          nickName: 朝夕。
                          source: 0
                          type: 2
                          content: '[白眼][白眼]'
                          createTime: 1672382745
                          commentId: 1057
                          replyCommentId: 1025
                          isNotRichText: 1
                        - userName: wxid_5042230422112
                          nickName: A 梦里梦见梦不见的梦
                          source: 0
                          type: 2
                          content: 你怎么个贾汪民政局的，你不是贾汪的不是吗
                          createTime: 1672386176
                          commentId: 1089
                          replyCommentId: 0
                          isNotRichText: 1
                      withUserCount: 0
                      withUserList: null
                    - id: 14020472144428995000
                      userName: zhangchuan2288
                      nickName: 朝夕。
                      createTime: 1671370523
                      snsXml: >-
                        <TimelineObject><id>14020472144428994892</id><username>zhangchuan2288</username><createTime>1671370523</createTime><contentDesc>各位亲朋好友，非常抱歉的遥知大家：&#x0A;&#x0A;受疫情影响，我们原定于1月15日的婚礼将延期举行，后续举办时间另行通知。&#x0A;&#x0A;虽有遗憾，但比起婚礼，我们更担心各位亲友的安全。&#x0A;&#x0A;愿山河无恙，人间皆安，&#x0A;&#x0A;非常时期，我们一起共度时艰，待到春花烂漫，繁华与共，再次邀请各位亲友共享我们这份延迟的喜悦。</contentDesc><contentDescShowType>0</contentDescShowType><contentDescScene>3</contentDescScene><private>0</private><sightFolded>0</sightFolded><showFlag>0</showFlag><appInfo><id></id><version></version><appName></appName><installUrl></installUrl><fromUrl></fromUrl><isForceUpdate>0</isForceUpdate></appInfo><sourceUserName></sourceUserName><sourceNickName></sourceNickName><statisticsData></statisticsData><statExtStr></statExtStr><ContentObject><contentStyle>2</contentStyle><title></title><description></description><mediaList></mediaList><contentUrl></contentUrl></ContentObject><actionInfo><appMsg><messageAction></messageAction></appMsg></actionInfo><location
                        poiClassifyId="" poiName="" poiAddress=""
                        poiClassifyType="0"
                        city=""></location><publicUserName></publicUserName><streamvideo><streamvideourl></streamvideourl><streamvideothumburl></streamvideothumburl><streamvideoweburl></streamvideoweburl></streamvideo></TimelineObject>
                      likeCount: 10
                      likeList:
                        - userName: zhangchuan2288
                          nickName: 朝夕。
                          source: 0
                          type: 1
                          createTime: 1671371441
                        - userName: wxid_7tmw73r2hpjq22
                          nickName: 呵呵
                          source: 0
                          type: 1
                          createTime: 1671371892
                        - userName: wxid_9ctin4xzpbqz21
                          nickName: 远方
                          source: 0
                          type: 1
                          createTime: 1671372088
                        - userName: wxid_0rp825czl4o722
                          nickName: 小小晴仔🐳
                          source: 0
                          type: 1
                          createTime: 1671373801
                        - userName: wxid_ehcl9lv7l8rs22
                          nickName: X-zzzz
                          source: 0
                          type: 1
                          createTime: 1671374936
                        - userName: wxid_dwlzssmhbycr21
                          nickName: 曼妍美甲美睫美容养生会所
                          source: 0
                          type: 1
                          createTime: 1671375069
                        - userName: wxid_24n7es7cd9mv21
                          nickName: 落婲丶無痕
                          source: 0
                          type: 1
                          createTime: 1671377256
                        - userName: wxid_8112531125912
                          nickName: 王富贵
                          source: 0
                          type: 1
                          createTime: 1671379054
                        - userName: wxid_3tctjyoc91u322
                          nickName: 大乞丐
                          source: 0
                          type: 1
                          createTime: 1671408286
                        - userName: star911128
                          nickName: 咩咩咪丫
                          source: 0
                          type: 1
                          createTime: 1671408463
                      commentCount: 2
                      commentList:
                        - userName: wxid_bwtz9nn9yds422
                          nickName: 大鸭梨
                          source: 0
                          type: 2
                          content: 这书面通知写的很有文采[旺柴][旺柴]
                          createTime: 1671380865
                          commentId: 1
                          replyCommentId: 0
                          isNotRichText: 1
                        - userName: zhangchuan2288
                          nickName: 朝夕。
                          source: 0
                          type: 2
                          content: 毕竟只改了个日期[破涕为笑]
                          createTime: 1671412735
                          commentId: 33
                          replyCommentId: 1
                          isNotRichText: 1
                      withUserCount: 0
                      withUserList: null
          headers: {}
          x-apifox-name: 成功
      security: []
      x-apifox-folder: 基础API/朋友圈模块
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3475559/apis/api-139908348-run
components:
  schemas: {}
  securitySchemes: {}
servers:
  - url: http://218.78.116.24:10883
    description: 测试环境
security: []

```

# 某条朋友圈详情

## OpenAPI

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /gewe/v2/api/sns/snsDetails:
    post:
      summary: 某条朋友圈详情
      deprecated: false
      description: ''
      tags:
        - 基础API/朋友圈模块
      parameters:
        - name: X-GEWE-TOKEN
          in: header
          description: ''
          required: true
          example: '{{gewe-token}}'
          schema:
            type: string
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                appId:
                  type: string
                  description: 设备ID
                  additionalProperties: false
                snsId:
                  type: number
                  description: 朋友圈ID
              x-apifox-orders:
                - appId
                - snsId
              required:
                - appId
                - snsId
            example:
              appId: '{{appid}}'
              snsId: 14214000407987818000
      responses:
        '200':
          description: ''
          content:
            application/json:
              schema:
                type: object
                properties:
                  ret:
                    type: integer
                  msg:
                    type: string
                  data:
                    type: object
                    properties:
                      id:
                        type: integer
                        description: 朋友圈ID
                      userName:
                        type: string
                        description: 朋友圈作者的wxid
                      nickName:
                        type: string
                        description: 朋友圈作者的昵称
                      createTime:
                        type: integer
                        description: 发布时间
                      snsXml:
                        type: string
                        description: 朋友圈的xml，可用于转发朋友圈
                      likeCount:
                        type: integer
                        description: 点赞数
                      likeList:
                        type: array
                        items:
                          type: object
                          properties:
                            userName:
                              type: string
                              description: 点赞好友的wxid
                            nickName:
                              type: string
                              description: 点赞好友的昵称
                            source:
                              type: integer
                              description: 来源
                            type:
                              type: integer
                              description: 类型
                            createTime:
                              type: integer
                              description: 点赞时间
                          required:
                            - userName
                            - nickName
                            - source
                            - type
                            - createTime
                          x-apifox-orders:
                            - userName
                            - nickName
                            - source
                            - type
                            - createTime
                        description: 点赞好友的信息
                      commentCount:
                        type: integer
                        description: 评论数
                      commentList:
                        type: array
                        items:
                          type: object
                          properties:
                            userName:
                              type: string
                              description: 评论好友的wxid
                            nickName:
                              type: string
                              description: 评论好友的昵称
                            source:
                              type: integer
                              description: 来源
                            type:
                              type: integer
                              description: 类型
                            content:
                              type: string
                              description: 评论内容
                            createTime:
                              type: integer
                              description: 评论时间
                            commentId:
                              type: integer
                              description: 评论ID
                            replyCommentId:
                              type: integer
                              description: 回复的评论ID
                            isNotRichText:
                              type: integer
                          required:
                            - userName
                            - nickName
                            - source
                            - type
                            - content
                            - createTime
                            - commentId
                            - replyCommentId
                            - isNotRichText
                          x-apifox-orders:
                            - userName
                            - nickName
                            - source
                            - type
                            - content
                            - createTime
                            - commentId
                            - replyCommentId
                            - isNotRichText
                        description: 评论的内容
                      withUserCount:
                        type: integer
                        description: 提醒谁看的数量
                      withUserList:
                        type: 'null'
                        description: 提醒谁看的wxid
                    required:
                      - id
                      - userName
                      - nickName
                      - createTime
                      - snsXml
                      - likeCount
                      - likeList
                      - commentCount
                      - commentList
                      - withUserCount
                      - withUserList
                    x-apifox-orders:
                      - id
                      - userName
                      - nickName
                      - createTime
                      - snsXml
                      - likeCount
                      - likeList
                      - commentCount
                      - commentList
                      - withUserCount
                      - withUserList
                required:
                  - ret
                  - msg
                  - data
                x-apifox-orders:
                  - ret
                  - msg
                  - data
              example:
                ret: 200
                msg: 操作成功
                data:
                  id: 14214000407987818000
                  userName: zhangchuan2288
                  nickName: 朝夕。
                  createTime: 1694440890
                  snsXml: >-
                    <TimelineObject><id>14214000407987819068</id><username>zhangchuan2288</username><createTime>1694440890</createTime><contentDesc>搁置了一个月的战车，出门蹬一会被撞了，忘了躺地上，错失一个换车的机会。[苦涩][苦涩]</contentDesc><contentDescShowType>0</contentDescShowType><contentDescScene>3</contentDescScene><private>0</private><sightFolded>0</sightFolded><showFlag>0</showFlag><appInfo><id></id><version></version><appName></appName><installUrl></installUrl><fromUrl></fromUrl><isForceUpdate>0</isForceUpdate><isHidden>0</isHidden></appInfo><sourceUserName></sourceUserName><sourceNickName></sourceNickName><statisticsData></statisticsData><statExtStr></statExtStr><ContentObject><contentStyle>1</contentStyle><title></title><description></description><mediaList><media><id>14214000408859710018</id><type>2</type><title></title><description>搁置了一个月的战车，出门蹬一会被撞了，忘了躺地上，错失一个换车的机会。[苦涩][苦涩]</description><private>0</private><userData></userData><subType>0</subType><videoSize
                    width="1080" height="1920"></videoSize><url type="1"
                    md5="a9a21ec7afe3a51e1635cd4844de29bb"
                    videomd5="">http://shmmsns.qpic.cn/mmsns/FzeKA69P5uIdqPfQxp59LpevPpX0bJz1zbXSpiavc01kia9H4cic0dJbHbUEJDibB8jx2oXfnBuKhgg/0</url><thumb
                    type="1">http://shmmsns.qpic.cn/mmsns/FzeKA69P5uIdqPfQxp59LpevPpX0bJz1zbXSpiavc01kia9H4cic0dJbHbUEJDibB8jx2oXfnBuKhgg/150</thumb><size
                    width="1080.000000" height="1920.000000"
                    totalSize="223727"></size></media></mediaList><contentUrl></contentUrl></ContentObject><actionInfo><appMsg><messageAction></messageAction></appMsg></actionInfo><location
                    poiClassifyId="" poiName="" poiAddress=""
                    poiClassifyType="0"
                    city=""></location><publicUserName></publicUserName><streamvideo><streamvideourl></streamvideourl><streamvideothumburl></streamvideothumburl><streamvideoweburl></streamvideoweburl></streamvideo></TimelineObject>
                  likeCount: 4
                  likeList:
                    - userName: wxid_fym4i76rk40x12
                      nickName: 糖果
                      source: 0
                      type: 1
                      createTime: 1694440920
                    - userName: wxid_bhf0vdaei64u21
                      nickName: 挽风～
                      source: 0
                      type: 1
                      createTime: 1694441103
                    - userName: wxid_jcllrz90yht022
                      nickName: ^^辻弌^^
                      source: 0
                      type: 1
                      createTime: 1694441218
                    - userName: wxid_5hafab2a85yk12
                      nickName: 丶zoū zoú zoǔ zoù 👾
                      source: 0
                      type: 1
                      createTime: 1694455325
                  commentCount: 19
                  commentList:
                    - userName: wxid_6xi2yuy30id422
                      nickName: ME
                      source: 0
                      type: 2
                      content: 去医院验伤 索赔
                      createTime: 1694441070
                      commentId: 1
                      replyCommentId: 0
                      isNotRichText: 1
                    - userName: wxid_7538985368812
                      nickName: 故事的小黄花
                      source: 0
                      type: 2
                      content: 懂车帝没下载好？
                      createTime: 1694441111
                      commentId: 33
                      replyCommentId: 0
                      isNotRichText: 1
                    - userName: zhangchuan2288
                      nickName: 朝夕。
                      source: 0
                      type: 2
                      content: 来不及了，赔了点钱就让走了[捂脸]
                      createTime: 1694441270
                      commentId: 65
                      replyCommentId: 1
                      isNotRichText: 1
                    - userName: wxid_bhf0vdaei64u21
                      nickName: 挽风～
                      source: 0
                      type: 2
                      content: 对方在想:那人竟然没躺地上，感觉他像自己赚了一个亿那么开心[破涕为笑]
                      createTime: 1694441274
                      commentId: 97
                      replyCommentId: 0
                      isNotRichText: 1
                    - userName: wxid_6xi2yuy30id422
                      nickName: ME
                      source: 0
                      type: 2
                      content: 报警 你说验出严重的伤了
                      createTime: 1694441302
                      commentId: 129
                      replyCommentId: 65
                      isNotRichText: 1
                    - userName: zhangchuan2288
                      nickName: 朝夕。
                      source: 0
                      type: 2
                      content: 没来得及，错失良机
                      createTime: 1694441314
                      commentId: 161
                      replyCommentId: 33
                      isNotRichText: 1
                    - userName: zhangchuan2288
                      nickName: 朝夕。
                      source: 0
                      type: 2
                      content: 我都看出来他的开心了😃
                      createTime: 1694441371
                      commentId: 193
                      replyCommentId: 97
                      isNotRichText: 1
                    - userName: zhangchuan2288
                      nickName: 朝夕。
                      source: 0
                      type: 2
                      content: 就是影响心情，倒是也没啥
                      createTime: 1694441407
                      commentId: 225
                      replyCommentId: 129
                      isNotRichText: 1
                    - userName: wxid_nasqrofbjvxa22
                      nickName: 灼
                      source: 0
                      type: 2
                      content: 车胎昨天刚爆[捂脸]
                      createTime: 1694441828
                      commentId: 259
                      replyCommentId: 0
                      isNotRichText: 1
                    - userName: zhangchuan2288
                      nickName: 朝夕。
                      source: 0
                      type: 2
                      content: 正好歇着
                      createTime: 1694442074
                      commentId: 289
                      replyCommentId: 259
                      isNotRichText: 1
                    - userName: wxid_98pjjzpiisi721
                      nickName: 宋端雅
                      source: 0
                      type: 2
                      content: 去医院，你有保险，咱不怕
                      createTime: 1694442081
                      commentId: 321
                      replyCommentId: 0
                      isNotRichText: 1
                    - userName: zhangchuan2288
                      nickName: 朝夕。
                      source: 0
                      type: 2
                      content: 忘了这茬。有没有自行车险，我买一个[破涕为笑][破涕为笑]
                      createTime: 1694442193
                      commentId: 353
                      replyCommentId: 321
                      isNotRichText: 1
                    - userName: wxid_98pjjzpiisi721
                      nickName: 宋端雅
                      source: 0
                      type: 2
                      content: 价值太低了，不值当的[捂脸]
                      createTime: 1694442243
                      commentId: 385
                      replyCommentId: 353
                      isNotRichText: 1
                    - userName: wxid_nasqrofbjvxa22
                      nickName: 灼
                      source: 0
                      type: 2
                      content: 一个月爆了两次[苦涩]，都没法看小姑娘了
                      createTime: 1694442381
                      commentId: 419
                      replyCommentId: 289
                      isNotRichText: 1
                    - userName: zhangchuan2288
                      nickName: 朝夕。
                      source: 0
                      type: 2
                      content: 哪有小姑娘，我骑共享单车也得去
                      createTime: 1694442448
                      commentId: 449
                      replyCommentId: 419
                      isNotRichText: 1
                    - userName: wxid_nasqrofbjvxa22
                      nickName: 灼
                      source: 0
                      type: 2
                      content: 金龙湖，大龙湖，你来
                      createTime: 1694442524
                      commentId: 483
                      replyCommentId: 449
                      isNotRichText: 1
                    - userName: wxid_5042230422112
                      nickName: 文强
                      source: 0
                      type: 2
                      content: 我看你胖了，是把车轱辘压拍圈了吧
                      createTime: 1694488063
                      commentId: 513
                      replyCommentId: 0
                      isNotRichText: 1
                    - userName: zhangchuan2288
                      nickName: 朝夕。
                      source: 0
                      type: 2
                      content: 哎日，几年不见了，你不能来请我吃个饭吗
                      createTime: 1694488128
                      commentId: 545
                      replyCommentId: 513
                      isNotRichText: 1
                    - userName: wxid_5042230422112
                      nickName: 文强
                      source: 0
                      type: 2
                      content: 你个哪了
                      createTime: 1694488297
                      commentId: 577
                      replyCommentId: 545
                      isNotRichText: 1
                  withUserCount: 0
                  withUserList: null
          headers: {}
          x-apifox-name: 成功
      security: []
      x-apifox-folder: 基础API/朋友圈模块
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3475559/apis/api-139908349-run
components:
  schemas: {}
  securitySchemes: {}
servers:
  - url: http://218.78.116.24:10883
    description: 测试环境
security: []

```

# 评论/删除评论

> 在新设备登录后的1-3天内，您将无法使用朋友圈发布、点赞、评论等功能。在此期间，如果尝试进行这些操作，您将收到来自微信团队的提醒。请注意遵守相关规定。

## OpenAPI

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /gewe/v2/api/sns/commentSns:
    post:
      summary: 评论/删除评论
      deprecated: false
      description: >-
        在新设备登录后的1-3天内，您将无法使用朋友圈发布、点赞、评论等功能。在此期间，如果尝试进行这些操作，您将收到来自微信团队的提醒。请注意遵守相关规定。
      tags:
        - 基础API/朋友圈模块
      parameters:
        - name: X-GEWE-TOKEN
          in: header
          description: ''
          required: true
          example: '{{gewe-token}}'
          schema:
            type: string
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                appId:
                  type: string
                  description: 设备ID
                  additionalProperties: false
                snsId:
                  type: number
                  description: 朋友圈ID
                operType:
                  type: integer
                  description: 1评论 2删除评论
                wxid:
                  type: string
                  description: 评论的好友wxid
                commentId:
                  type: string
                  description: 回复某条评论或删除某条评论
                content:
                  type: string
                  description: 评论内容
              x-apifox-orders:
                - appId
                - snsId
                - operType
                - wxid
                - commentId
                - content
              required:
                - appId
                - snsId
                - operType
                - wxid
            example:
              appId: '{{appid}}'
              snsId: 14287710653886042000
              operType: 2
              wxid: wxid_4mb3zx0q09fq21
              commentId: 1
              content: ''
      responses:
        '200':
          description: ''
          content:
            application/json:
              schema:
                type: object
                properties:
                  ret:
                    type: integer
                  msg:
                    type: string
                required:
                  - ret
                  - msg
                x-apifox-orders:
                  - ret
                  - msg
              example:
                ret: 200
                msg: 操作成功
          headers: {}
          x-apifox-name: 成功
      security: []
      x-apifox-folder: 基础API/朋友圈模块
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3475559/apis/api-139908350-run
components:
  schemas: {}
  securitySchemes: {}
servers:
  - url: http://218.78.116.24:10883
    description: 测试环境
security: []

```