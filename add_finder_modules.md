# 关注

## OpenAPI

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /gewe/v2/api/finder/follow:
    post:
      summary: 关注
      deprecated: false
      description: ''
      tags:
        - 基础API/视频号模块
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
                myUserName:
                  type: string
                  description: 自己的username
                myRoleType:
                  type: integer
                  description: 自己的roletype
                toUserName:
                  type: string
                  description: 对方的username
                opType:
                  type: integer
                  description: 1:关注   2:取消关注
                searchInfo:
                  type: object
                  properties:
                    cookies:
                      type: string
                    docId:
                      type: string
                    searchId:
                      type: string
                  x-apifox-orders:
                    - cookies
                    - docId
                    - searchId
                  required:
                    - cookies
                    - searchId
                    - docId
                  description: 如果是通过搜索渠道关注，则把搜索接口返回的cookies、searchId、docId传进来
              required:
                - appId
                - myUserName
                - myRoleType
                - opType
                - toUserName
              x-apifox-orders:
                - appId
                - myUserName
                - myRoleType
                - toUserName
                - opType
                - searchInfo
            example:
              appId: '{{appid}}'
              proxyIp: ''
              myUserName: >-
                v2_060000231003b20faec8c7e28811c4d5cc0ded37b0779c48c759a7446a87688c2774e5300c32@finder
              myRoleType: 3
              opType: 1
              toUserName: >-
                v2_060000231003b20faec8c6e18f10c7d6c903ec3db0776955d3d97c6b329d6aa58693bcdb7ad1@finder
              searchInfo:
                cookies: ''
                searchId: ''
                docId: ''
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
                      username:
                        type: string
                        description: 对方的username
                      nickname:
                        type: string
                        description: 昵称
                      headUrl:
                        type: string
                        description: 头像
                      signature:
                        type: string
                        description: 简介
                      followFlag:
                        type: integer
                      authInfo:
                        type: object
                        properties: {}
                        x-apifox-orders: []
                      coverImgUrl:
                        type: string
                      spamStatus:
                        type: integer
                      extFlag:
                        type: integer
                      extInfo:
                        type: object
                        properties:
                          country:
                            type: string
                            description: 国家
                          province:
                            type: string
                            description: 省份
                          city:
                            type: string
                            description: 城市
                          sex:
                            type: integer
                            description: 性别
                        required:
                          - country
                          - province
                          - city
                          - sex
                        x-apifox-orders:
                          - country
                          - province
                          - city
                          - sex
                      liveStatus:
                        type: integer
                      liveCoverImgUrl:
                        type: string
                      liveInfo:
                        type: object
                        properties:
                          anchorStatusFlag:
                            type: integer
                          switchFlag:
                            type: integer
                          lotterySetting:
                            type: object
                            properties:
                              settingFlag:
                                type: integer
                              attendType:
                                type: integer
                            required:
                              - settingFlag
                              - attendType
                            x-apifox-orders:
                              - settingFlag
                              - attendType
                        required:
                          - anchorStatusFlag
                          - switchFlag
                          - lotterySetting
                        x-apifox-orders:
                          - anchorStatusFlag
                          - switchFlag
                          - lotterySetting
                      status:
                        type: integer
                    required:
                      - username
                      - nickname
                      - headUrl
                      - signature
                      - followFlag
                      - authInfo
                      - coverImgUrl
                      - spamStatus
                      - extFlag
                      - extInfo
                      - liveStatus
                      - liveCoverImgUrl
                      - liveInfo
                      - status
                    x-apifox-orders:
                      - username
                      - nickname
                      - headUrl
                      - signature
                      - followFlag
                      - authInfo
                      - coverImgUrl
                      - spamStatus
                      - extFlag
                      - extInfo
                      - liveStatus
                      - liveCoverImgUrl
                      - liveInfo
                      - status
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
                  username: >-
                    v2_060000231003b20faec8c6e18f10c7d6c903ec3db0776955d3d97c6b329d6aa58693bcdb7ad1@finder
                  nickname: 朝夕v
                  headUrl: >-
                    https://wx.qlogo.cn/finderhead/ver_1/TDibw5X5xTzpMW9D4GE0YnYUMqPAspF0AibTwhdSFWjyt2tZCMuLVon1PIT6aGulvzvlSZPkDcT06NB6D1eoLicYBKiaBCRDXZJSMEErIGQkQJ8/0
                  signature: 。。。
                  followFlag: 1
                  authInfo: {}
                  coverImgUrl: ''
                  spamStatus: 0
                  extFlag: 262156
                  extInfo:
                    country: CN
                    province: Jiangsu
                    city: Xuzhou
                    sex: 2
                  liveStatus: 2
                  liveCoverImgUrl: >-
                    http://wxapp.tc.qq.com/251/20350/stodownload?m=be88b1cb981aa72b3328ccbd22a58e0b&filekey=30340201010420301e020200fb040253480410be88b1cb981aa72b3328ccbd22a58e0b02022814040d00000004627466730000000132&hy=SH&storeid=5649443df0009b8a38399cc84000000fb00004f7e534815c008e0b08dc805c&dotrans=0&bizid=1023
                  liveInfo:
                    anchorStatusFlag: 133248
                    switchFlag: 53727
                    lotterySetting:
                      settingFlag: 0
                      attendType: 4
                  status: 0
          headers: {}
          x-apifox-name: 成功
      security: []
      x-apifox-folder: 基础API/视频号模块
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3475559/apis/api-144566017-run
components:
  schemas: {}
  securitySchemes: {}
servers:
  - url: http://218.78.116.24:10883
    description: 测试环境
security: []

```

# 评论

## OpenAPI

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /gewe/v2/api/finder/comment:
    post:
      summary: 评论
      deprecated: false
      description: ''
      tags:
        - 基础API/视频号模块
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
                proxyIp:
                  type: string
                myUserName:
                  type: string
                  description: 自己的username
                opType:
                  type: integer
                  description: 0评论 1删除评论
                objectNonceId:
                  type: string
                  description: 视频号的objectNonceId
                sessionBuffer:
                  type: string
                  description: 视频号的sessionBuffer
                objectId:
                  type: integer
                  description: 视频号的objectId
                myRoleType:
                  type: integer
                  description: 自己的roletype
                content:
                  type: string
                  description: 评论内容
                commentId:
                  type: string
                  description: 评论id
                replyUserName:
                  type: string
                  description: 回复评论的username
                refCommentId:
                  type: integer
                rootCommentId:
                  type: integer
              required:
                - appId
                - proxyIp
                - myUserName
                - opType
                - objectNonceId
                - sessionBuffer
                - objectId
                - myRoleType
                - content
                - commentId
                - replyUserName
                - refCommentId
                - rootCommentId
              x-apifox-orders:
                - appId
                - content
                - objectId
                - sessionBuffer
                - objectNonceId
                - opType
                - myUserName
                - myRoleType
                - replyUserName
                - refCommentId
                - rootCommentId
                - proxyIp
                - commentId
            example:
              appId: '{{appid}}'
              proxyIp: ''
              myUserName: >-
                v2_060000231003b20faec8c7e28811c4d5cc0ded37b0779c48c759a7446a87688c2774e5300c32@finder
              opType: 0
              objectNonceId: '16628169456191691547_0_39_2_1_0'
              sessionBuffer: >-
                eyJjdXJfbGlrZV9jb3VudCI6MiwiY3VyX2NvbW1lbnRfY291bnQiOjUsInJlY2FsbF90eXBlcyI6W10sImRlbGl2ZXJ5X3NjZW5lIjoyLCJkZWxpdmVyeV90aW1lIjoxNzA2MDg2ODE2LCJzZXRfY29uZGl0aW9uX2ZsYWciOjksImZyaWVuZF9jb21tZW50X2luZm8iOnsibGFzdF9mcmllbmRfdXNlcm5hbWUiOiJ6aGFuZ2NodWFuMjI4OCIsImxhc3RfZnJpZW5kX2xpa2VfdGltZSI6MTcwMzcyNjI4OH0sInRvdGFsX2ZyaWVuZF9saWtlX2NvdW50IjoxLCJyZWNhbGxfaW5kZXgiOltdLCJtZWRpYV90eXBlIjoyLCJjcmVhdGVfdGltZSI6MTY5MjE4MDMzNSwicmVjYWxsX2luZm8iOltdLCJvZmxhZyI6NDA5NzYsImlkYyI6MSwiZGV2aWNlX3R5cGVfaWQiOjEzLCJkZXZpY2VfcGxhdGZvcm0iOiJpUGFkMTMsNyIsImZlZWRfcG9zIjowLCJjbGllbnRfcmVwb3J0X2J1ZmYiOiJ7XCJpZl9zcGxpdF9zY3JlZW5faXBhZFwiOjAsXCJlbnRlclNvdXJjZUluZm9cIjpcIntcXFwiZmluZGVydXNlcm5hbWVcXFwiOlxcXCJcXFwiLFxcXCJmZWVkaWRcXFwiOlxcXCJcXFwifVwiLFwiZXh0cmFpbmZvXCI6XCJ7XFxuIFxcXCJyZWdjb3VudHJ5XFxcIiA6IFxcXCJDTlxcXCJcXG59XCIsXCJzZXNzaW9uSWRcIjpcIjEwMV8xNzA2MDg2ODA1NTE3IyQwXzE3MDYwODY3OTI4ODEjXCIsXCJqdW1wSWRcIjp7XCJ0cmFjZWlkXCI6XCJcIixcInNvdXJjZWlkXCI6XCJcIn19IiwiY29tbWVudF9zY2VuZSI6MzksIm9iamVjdF9pZCI6MTQxOTUwMzc1MDI5NzAwMDU4MjIsImZpbmRlcl91aW4iOjEzMTA0ODA0MjY5NDM3NzA5LCJnZW9oYXNoIjozMzc3Njk5NzIwNTI3ODcyLCJlbnRyYW5jZV9zY2VuZSI6MSwiY2FyZF90eXBlIjoxLCJleHB0X2ZsYWciOjMwMDY3Njk5LCJ1c2VyX21vZGVsX2ZsYWciOjgsImlzX2ZyaWVuZCI6dHJ1ZSwiY3R4X2lkIjoiMS0xLTIwLWJmNmEyNzQzYzhiNTM1ZjJlNmY2MzEyZjUwZjM3M2VjMTcwNjA4NjgxMDY0MyIsImFkX2ZsYWciOjQsImVyaWwiOltdLCJwZ2tleXMiOltdLCJzY2lkIjoiZmRiMjg0MGMtYmE5Ni0xMWVlLTg0MDAtZGI5NzlkZmJlZTYwIn0=
              objectId: 14195037502970006000
              myRoleType: 3
              content: 评论内容
              commentId: '14484855201138809377'
              replyUserName: ''
              refCommentId: 0
              rootCommentId: 0
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
                      commentId:
                        type: 'null'
                        description: 评论ID
                    required:
                      - commentId
                    x-apifox-orders:
                      - commentId
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
                  commentId: null
          headers: {}
          x-apifox-name: 成功
      security: []
      x-apifox-folder: 基础API/视频号模块
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3475559/apis/api-144581776-run
components:
  schemas: {}
  securitySchemes: {}
servers:
  - url: http://218.78.116.24:10883
    description: 测试环境
security: []

```

# 浏览

## OpenAPI

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /gewe/v2/api/finder/browse:
    post:
      summary: 浏览
      deprecated: false
      description: ''
      tags:
        - 基础API/视频号模块
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
                objectId:
                  type: integer
                  description: 视频号的objectId
                sessionBuffer:
                  type: string
                  description: 视频号的sessionBuffer
                objectNonceId:
                  type: string
                  description: 视频号的objectNonceId
                myUserName:
                  type: string
                  description: 自己的username
                myRoleType:
                  type: integer
                  description: 自己的roletype
              required:
                - appId
                - myUserName
                - objectNonceId
                - objectId
                - myRoleType
              x-apifox-orders:
                - appId
                - objectId
                - sessionBuffer
                - objectNonceId
                - myUserName
                - myRoleType
            example:
              appId: '{{appid}}'
              proxyIp: ''
              myUserName: >-
                v2_060000231003b20faec8c7e28811c4d5cc0ded37b0779c48c759a7446a87688c2774e5300c32@finder
              objectNonceId: '16628169456191691547_0_39_2_1_0'
              sessionBuffer: ''
              objectId: 14195037502970006000
              myRoleType: 3
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
              example:
                ret: 200
                msg: 操作成功
          headers: {}
          x-apifox-name: 成功
      security: []
      x-apifox-folder: 基础API/视频号模块
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3475559/apis/api-144595581-run
components:
  schemas: {}
  securitySchemes: {}
servers:
  - url: http://218.78.116.24:10883
    description: 测试环境
security: []

```

# 发布视频

## OpenAPI

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /gewe/v2/api/finder/publishFinder:
    post:
      summary: 发布视频
      deprecated: false
      description: ''
      tags:
        - 基础API/视频号模块
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
                videoUrl:
                  type: string
                  description: 视频链接地址
                thumbUrl:
                  type: string
                  description: 封面链接地址
                width:
                  type: integer
                  description: 视频宽度
                height:
                  type: integer
                  description: 视频高度
                playLen:
                  type: integer
                  description: 视频播放时长，单位秒
                topic:
                  type: array
                  items:
                    type: string
                  description: 视频号话题
                description:
                  type: string
                  description: 视频号描述
                myUserName:
                  type: string
                  description: 自己的username
                myRoleType:
                  type: integer
                  description: 自己的roletype
              required:
                - appId
                - videoUrl
                - thumbUrl
                - myRoleType
                - myUserName
                - description
              x-apifox-orders:
                - appId
                - videoUrl
                - thumbUrl
                - width
                - height
                - playLen
                - topic
                - description
                - myUserName
                - myRoleType
            example:
              appId: '{{appid}}'
              proxyIp: ''
              videoUrl: >-
                https://scrm-1308498490.cos.ap-shanghai.myqcloud.com/pkg/436fa030-18a45a6e917.mp4
              playLen: 48
              height: 13
              width: 76
              thumbUrl: http://dummyimage.com/400x400
              myRoleType: 3
              topic:
                - '#hh'
                - '#哈哈'
              myUserName: >-
                v2_060000231003b20faec8c7e28811c4d5cc0ded37b0779c48c759a7446a87688c2774e5300c32@finder
              description: hhh
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
                        description: 作品ID
                    required:
                      - id
                    x-apifox-orders:
                      - id
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
                      id: 14381299491553024000
                '2':
                  summary: 异常示例
                  value:
                    ret: 500
                    msg: 发布视频失败
                    data:
                      code: '-4013'
                      msg: null
          headers: {}
          x-apifox-name: 成功
        '500':
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
                      code:
                        type: string
                      msg:
                        type: 'null'
                    required:
                      - code
                      - msg
                required:
                  - ret
                  - msg
                  - data
          headers: {}
          x-apifox-name: 服务器错误
      security: []
      x-apifox-folder: 基础API/视频号模块
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3475559/apis/api-144557553-run
components:
  schemas: {}
  securitySchemes: {}
servers:
  - url: http://218.78.116.24:10883
    description: 测试环境
security: []

```

# 发布视频-新

## OpenAPI

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /gewe/v2/api/finder/publishFinderWeb:
    post:
      summary: 发布视频-新
      deprecated: false
      description: ''
      tags:
        - 基础API/视频号模块
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
                title:
                  type: string
                  x-apifox-mock: 标题
                videoUrl:
                  type: string
                  x-apifox-mock: 视频地址
                thumbUrl:
                  type: string
                  x-apifox-mock: 封面地址
                description:
                  type: string
                  x-apifox-mock: 描述
              required:
                - appId
                - title
                - videoUrl
                - thumbUrl
                - description
              x-apifox-orders:
                - appId
                - title
                - videoUrl
                - thumbUrl
                - description
            example:
              appId: '{{appid}}'
              title: test测试
              videoUrl: >-
                https://scrm-1308498490.cos.ap-shanghai.myqcloud.com/test/d7c616569ac342ad1fa8e3301682844e.mp4?q-sign-algorithm=sha1&q-ak=AKIDmOkqfDUUDfqjMincBSSAbleGaeQv96mB&q-sign-time=1735795742;10375709342&q-key-time=1735795742;10375709342&q-header-list=&q-url-param-list=&q-signature=10a1f7548fa65c8a20c2958f18b68f0db9dfd13d
              thumbUrl: >-
                https://scrm-1308498490.cos.ap-shanghai.myqcloud.com/test/photo_2024-10-05_12-15-43.jpg?q-sign-algorithm=sha1&q-ak=AKIDmOkqfDUUDfqjMincBSSAbleGaeQv96mB&q-sign-time=1735797655;10375711255&q-key-time=1735797655;10375711255&q-header-list=&q-url-param-list=&q-signature=5f0a4253c08b6d14c018aa1fd9295c129acbb64c
              description: '#测试##123#'
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
                        description: 作品ID
                    required:
                      - id
                    x-apifox-orders:
                      - id
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
                      id: 14381299491553024000
                '2':
                  summary: 异常示例
                  value:
                    ret: 500
                    msg: 发布视频失败
                    data:
                      code: '-4013'
                      msg: null
          headers: {}
          x-apifox-name: 成功
        '500':
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
                      code:
                        type: string
                      msg:
                        type: 'null'
                    required:
                      - code
                      - msg
                required:
                  - ret
                  - msg
                  - data
          headers: {}
          x-apifox-name: 服务器错误
      security: []
      x-apifox-folder: 基础API/视频号模块
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3475559/apis/api-288633556-run
components:
  schemas: {}
  securitySchemes: {}
servers:
  - url: http://218.78.116.24:10883
    description: 测试环境
security: []

```

# 用户主页

> 注：接口返回的视频id 通过工具测试会出现精度丢失的现象，如id以000结尾则表示精度丢失，精度丢失解决方式是将返回报文格式改成Raw或Text

## OpenAPI

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /gewe/v2/api/finder/userPage:
    post:
      summary: 用户主页
      deprecated: false
      description: 注：接口返回的视频id 通过工具测试会出现精度丢失的现象，如id以000结尾则表示精度丢失，精度丢失解决方式是将返回报文格式改成Raw或Text
      tags:
        - 基础API/视频号模块
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
                toUserName:
                  type: string
                  description: 用户的username
                lastBuffer:
                  type: string
                  description: 首次传空，后续传接口返回的lastBuffer
                maxId:
                  type: integer
                  description: 首次传0，后续传响应结果中最后一条的id
                searchInfo:
                  type: object
                  properties:
                    cookies:
                      type: string
                    searchId:
                      type: string
                  x-apifox-orders:
                    - cookies
                    - searchId
                  description: 如果是通过搜索渠道获取用户主页，则把搜索接口返回的cookies、searchId传进来
              required:
                - appId
                - toUserName
              x-apifox-orders:
                - appId
                - toUserName
                - lastBuffer
                - maxId
                - searchInfo
            example:
              appId: '{{appid}}'
              proxyIp: ''
              lastBuffer: ''
              toUserName: >-
                v2_060000231003b20faec8c6e18f10c7d6c903ec3db0776955d3d97c6b329d6aa58693bcdb7ad1@finder
              maxId: 0
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
                      object:
                        type: array
                        items:
                          type: object
                          properties:
                            id:
                              type: integer
                              description: 作品ID
                            nickname:
                              type: string
                              description: 昵称
                            username:
                              type: string
                              description: username
                            objectDesc:
                              type: object
                              properties:
                                description:
                                  type: string
                                media:
                                  type: array
                                  items:
                                    type: object
                                    properties:
                                      Url:
                                        type: string
                                      ThumbUrl:
                                        type: string
                                      MediaType:
                                        type: integer
                                      VideoPlayLen:
                                        type: integer
                                      Width:
                                        type: integer
                                      Height:
                                        type: integer
                                      Md5Sum:
                                        type: string
                                      FileSize:
                                        type: integer
                                      Bitrate:
                                        type: integer
                                      coverUrl:
                                        type: string
                                      decodeKey:
                                        type: string
                                      urlToken:
                                        type: string
                                      thumbUrlToken:
                                        type: string
                                      codecInfo:
                                        type: object
                                        properties:
                                          thumbScore:
                                            type: integer
                                          hdimgScore:
                                            type: integer
                                        required:
                                          - thumbScore
                                          - hdimgScore
                                        x-apifox-orders:
                                          - thumbScore
                                          - hdimgScore
                                      fullThumbUrl:
                                        type: string
                                      fullThumbUrlToken:
                                        type: string
                                      fullCoverUrl:
                                        type: string
                                      liveCoverImgs:
                                        type: array
                                        items:
                                          type: object
                                          properties:
                                            ThumbUrl:
                                              type: string
                                            FileSize:
                                              type: integer
                                            Width:
                                              type: integer
                                            Height:
                                              type: integer
                                            Bitrate:
                                              type: integer
                                          required:
                                            - ThumbUrl
                                            - FileSize
                                            - Width
                                            - Height
                                            - Bitrate
                                          x-apifox-orders:
                                            - ThumbUrl
                                            - FileSize
                                            - Width
                                            - Height
                                            - Bitrate
                                      cardShowStyle:
                                        type: integer
                                      dynamicRangeType:
                                        type: integer
                                      videoType:
                                        type: integer
                                    required:
                                      - Url
                                      - ThumbUrl
                                      - MediaType
                                      - VideoPlayLen
                                      - Width
                                      - Height
                                      - Md5Sum
                                      - FileSize
                                      - Bitrate
                                      - coverUrl
                                      - decodeKey
                                      - urlToken
                                      - thumbUrlToken
                                      - codecInfo
                                      - fullThumbUrl
                                      - fullThumbUrlToken
                                      - fullCoverUrl
                                      - liveCoverImgs
                                      - cardShowStyle
                                      - dynamicRangeType
                                      - videoType
                                    x-apifox-orders:
                                      - Url
                                      - ThumbUrl
                                      - MediaType
                                      - VideoPlayLen
                                      - Width
                                      - Height
                                      - Md5Sum
                                      - FileSize
                                      - Bitrate
                                      - coverUrl
                                      - decodeKey
                                      - urlToken
                                      - thumbUrlToken
                                      - codecInfo
                                      - fullThumbUrl
                                      - fullThumbUrlToken
                                      - fullCoverUrl
                                      - liveCoverImgs
                                      - cardShowStyle
                                      - dynamicRangeType
                                      - videoType
                                mediaType:
                                  type: integer
                                location:
                                  type: object
                                  properties: {}
                                  x-apifox-orders: []
                                extReading:
                                  type: object
                                  properties: {}
                                  x-apifox-orders: []
                                imgFeedBgmInfo:
                                  type: object
                                  properties:
                                    docId:
                                      type: string
                                    albumThumbUrl:
                                      type: string
                                    name:
                                      type: string
                                    artist:
                                      type: string
                                    albumName:
                                      type: string
                                    mediaStreamingUrl:
                                      type: string
                                  required:
                                    - docId
                                    - albumThumbUrl
                                    - name
                                    - artist
                                    - albumName
                                    - mediaStreamingUrl
                                  x-apifox-orders:
                                    - docId
                                    - albumThumbUrl
                                    - name
                                    - artist
                                    - albumName
                                    - mediaStreamingUrl
                                followPostInfo:
                                  type: object
                                  properties:
                                    musicInfo:
                                      type: object
                                      properties:
                                        docId:
                                          type: string
                                        albumThumbUrl:
                                          type: string
                                        name:
                                          type: string
                                        artist:
                                          type: string
                                        albumName:
                                          type: string
                                        mediaStreamingUrl:
                                          type: string
                                        miniappInfo:
                                          type: string
                                        webUrl:
                                          type: string
                                        floatThumbUrl:
                                          type: string
                                        chorusBegin:
                                          type: integer
                                        docType:
                                          type: integer
                                        songId:
                                          type: string
                                      required:
                                        - docId
                                        - albumThumbUrl
                                        - name
                                        - artist
                                        - albumName
                                        - mediaStreamingUrl
                                        - miniappInfo
                                        - webUrl
                                        - floatThumbUrl
                                        - chorusBegin
                                        - docType
                                        - songId
                                      x-apifox-orders:
                                        - docId
                                        - albumThumbUrl
                                        - name
                                        - artist
                                        - albumName
                                        - mediaStreamingUrl
                                        - miniappInfo
                                        - webUrl
                                        - floatThumbUrl
                                        - chorusBegin
                                        - docType
                                        - songId
                                    groupId:
                                      type: string
                                    hasBgm:
                                      type: integer
                                  required:
                                    - musicInfo
                                    - groupId
                                    - hasBgm
                                  x-apifox-orders:
                                    - musicInfo
                                    - groupId
                                    - hasBgm
                                fromApp:
                                  type: object
                                  properties: {}
                                  x-apifox-orders: []
                                event:
                                  type: object
                                  properties: {}
                                  x-apifox-orders: []
                                mvInfo:
                                  type: object
                                  properties: {}
                                  x-apifox-orders: []
                                draftObjectId:
                                  type: integer
                                clientDraftExtInfo:
                                  type: object
                                  properties:
                                    lbsFlagType:
                                      type: integer
                                    videoMusicId:
                                      type: string
                                  required:
                                    - lbsFlagType
                                    - videoMusicId
                                  x-apifox-orders:
                                    - lbsFlagType
                                    - videoMusicId
                                generalReportInfo:
                                  type: object
                                  properties: {}
                                  x-apifox-orders: []
                                posterLocation:
                                  type: object
                                  properties:
                                    longitude:
                                      type: number
                                    latitude:
                                      type: number
                                    city:
                                      type: string
                                  required:
                                    - longitude
                                    - latitude
                                    - city
                                  x-apifox-orders:
                                    - longitude
                                    - latitude
                                    - city
                                shortTitle:
                                  type: array
                                  items:
                                    type: string
                                originalInfoDesc:
                                  type: object
                                  properties: {}
                                  x-apifox-orders: []
                                finderNewlifeDesc:
                                  type: object
                                  properties: {}
                                  x-apifox-orders: []
                              required:
                                - description
                                - media
                                - mediaType
                                - location
                                - extReading
                                - imgFeedBgmInfo
                                - followPostInfo
                                - fromApp
                                - event
                                - mvInfo
                                - draftObjectId
                                - clientDraftExtInfo
                                - generalReportInfo
                                - posterLocation
                                - shortTitle
                                - originalInfoDesc
                                - finderNewlifeDesc
                              x-apifox-orders:
                                - description
                                - media
                                - mediaType
                                - location
                                - extReading
                                - imgFeedBgmInfo
                                - followPostInfo
                                - fromApp
                                - event
                                - mvInfo
                                - draftObjectId
                                - clientDraftExtInfo
                                - generalReportInfo
                                - posterLocation
                                - shortTitle
                                - originalInfoDesc
                                - finderNewlifeDesc
                            createtime:
                              type: integer
                              description: 创建时间
                            likeList:
                              type: array
                              items:
                                type: string
                            forwardCount:
                              type: integer
                              description: 转发次数
                            contact:
                              type: object
                              properties:
                                username:
                                  type: string
                                  description: username
                                nickname:
                                  type: string
                                  description: 昵称
                                headUrl:
                                  type: string
                                  description: 头像
                                seq:
                                  type: integer
                                signature:
                                  type: string
                                  description: 简介
                                followFlag:
                                  type: integer
                                authInfo:
                                  type: object
                                  properties: {}
                                  x-apifox-orders: []
                                coverImgUrl:
                                  type: string
                                spamStatus:
                                  type: integer
                                extFlag:
                                  type: integer
                                extInfo:
                                  type: object
                                  properties:
                                    country:
                                      type: string
                                      description: 国家
                                    province:
                                      type: string
                                      description: 省份
                                    city:
                                      type: string
                                      description: 城市
                                    sex:
                                      type: integer
                                      description: 性别
                                  required:
                                    - country
                                    - province
                                    - city
                                    - sex
                                  x-apifox-orders:
                                    - country
                                    - province
                                    - city
                                    - sex
                                  description: 扩展信息
                                liveStatus:
                                  type: integer
                                liveCoverImgUrl:
                                  type: string
                                liveInfo:
                                  type: object
                                  properties:
                                    anchorStatusFlag:
                                      type: integer
                                    switchFlag:
                                      type: integer
                                    lotterySetting:
                                      type: object
                                      properties:
                                        settingFlag:
                                          type: integer
                                        attendType:
                                          type: integer
                                      required:
                                        - settingFlag
                                        - attendType
                                      x-apifox-orders:
                                        - settingFlag
                                        - attendType
                                  required:
                                    - anchorStatusFlag
                                    - switchFlag
                                    - lotterySetting
                                  x-apifox-orders:
                                    - anchorStatusFlag
                                    - switchFlag
                                    - lotterySetting
                                friendFollowCount:
                                  type: integer
                                oneTimeFlag:
                                  type: integer
                                status:
                                  type: integer
                              required:
                                - username
                                - nickname
                                - headUrl
                                - seq
                                - signature
                                - followFlag
                                - authInfo
                                - coverImgUrl
                                - spamStatus
                                - extFlag
                                - extInfo
                                - liveStatus
                                - liveCoverImgUrl
                                - liveInfo
                                - friendFollowCount
                                - oneTimeFlag
                                - status
                              x-apifox-orders:
                                - username
                                - nickname
                                - headUrl
                                - seq
                                - signature
                                - followFlag
                                - authInfo
                                - coverImgUrl
                                - spamStatus
                                - extFlag
                                - extInfo
                                - liveStatus
                                - liveCoverImgUrl
                                - liveInfo
                                - friendFollowCount
                                - oneTimeFlag
                                - status
                              description: 作者信息
                            displayid:
                              type: integer
                            likeCount:
                              type: integer
                              description: 点赞数
                            commentCount:
                              type: integer
                              description: 评论数
                            deletetime:
                              type: integer
                            friendLikeCount:
                              type: integer
                              description: 好友点赞数
                            objectNonceId:
                              type: string
                              description: 对象NonceId
                            objectStatus:
                              type: integer
                            sendShareFavWording:
                              type: string
                            originalFlag:
                              type: integer
                            secondaryShowFlag:
                              type: integer
                            sessionBuffer:
                              type: string
                            favCount:
                              type: integer
                              description: 收藏数量
                            urlValidTime:
                              type: integer
                            forwardStyle:
                              type: integer
                            permissionFlag:
                              type: integer
                            attachmentList:
                              type: object
                              properties: {}
                              x-apifox-orders: []
                            objectType:
                              type: integer
                            followFeedCount:
                              type: integer
                            verifyInfoBuf:
                              type: string
                            wxStatusRefCount:
                              type: integer
                            adFlag:
                              type: integer
                            tipsInfo:
                              type: object
                              properties: {}
                              x-apifox-orders: []
                            internalFeedbackUrl:
                              type: string
                            ringtoneCount:
                              type: integer
                            funcFlag:
                              type: integer
                            playhistoryInfo:
                              type: object
                              properties: {}
                              x-apifox-orders: []
                            flowCardRecommandReason:
                              type: object
                              properties: {}
                              x-apifox-orders: []
                            ipRegionInfo:
                              type: object
                              properties: {}
                              x-apifox-orders: []
                          x-apifox-orders:
                            - id
                            - nickname
                            - username
                            - objectDesc
                            - createtime
                            - likeList
                            - forwardCount
                            - contact
                            - displayid
                            - likeCount
                            - commentCount
                            - deletetime
                            - friendLikeCount
                            - objectNonceId
                            - objectStatus
                            - sendShareFavWording
                            - originalFlag
                            - secondaryShowFlag
                            - sessionBuffer
                            - favCount
                            - urlValidTime
                            - forwardStyle
                            - permissionFlag
                            - attachmentList
                            - objectType
                            - followFeedCount
                            - verifyInfoBuf
                            - wxStatusRefCount
                            - adFlag
                            - tipsInfo
                            - internalFeedbackUrl
                            - ringtoneCount
                            - funcFlag
                            - playhistoryInfo
                            - flowCardRecommandReason
                            - ipRegionInfo
                      finderUserInfo:
                        type: object
                        properties:
                          coverImgUrl:
                            type: string
                        required:
                          - coverImgUrl
                        x-apifox-orders:
                          - coverImgUrl
                      contact:
                        type: object
                        properties:
                          username:
                            type: string
                            description: username
                          nickname:
                            type: string
                            description: 昵称
                          headUrl:
                            type: string
                            description: 头像
                          signature:
                            type: string
                            description: 简介
                          followFlag:
                            type: integer
                          followTime:
                            type: integer
                            description: 关注时间
                          authInfo:
                            type: object
                            properties: {}
                            x-apifox-orders: []
                          coverImgUrl:
                            type: string
                          spamStatus:
                            type: integer
                          extFlag:
                            type: integer
                          extInfo:
                            type: object
                            properties:
                              country:
                                type: string
                                description: 国家
                              province:
                                type: string
                                description: 省份
                              city:
                                type: string
                                description: 城市
                              sex:
                                type: integer
                                description: 性别
                            required:
                              - country
                              - province
                              - city
                              - sex
                            x-apifox-orders:
                              - country
                              - province
                              - city
                              - sex
                            description: 扩展信息
                          liveStatus:
                            type: integer
                          liveCoverImgUrl:
                            type: string
                          liveInfo:
                            type: object
                            properties:
                              anchorStatusFlag:
                                type: integer
                              switchFlag:
                                type: integer
                              lotterySetting:
                                type: object
                                properties:
                                  settingFlag:
                                    type: integer
                                  attendType:
                                    type: integer
                                required:
                                  - settingFlag
                                  - attendType
                                x-apifox-orders:
                                  - settingFlag
                                  - attendType
                            required:
                              - anchorStatusFlag
                              - switchFlag
                              - lotterySetting
                            x-apifox-orders:
                              - anchorStatusFlag
                              - switchFlag
                              - lotterySetting
                          friendFollowCount:
                            type: integer
                            description: 好友关注数
                          oneTimeFlag:
                            type: integer
                          status:
                            type: integer
                        required:
                          - username
                          - nickname
                          - headUrl
                          - signature
                          - followFlag
                          - followTime
                          - authInfo
                          - coverImgUrl
                          - spamStatus
                          - extFlag
                          - extInfo
                          - liveStatus
                          - liveCoverImgUrl
                          - liveInfo
                          - friendFollowCount
                          - oneTimeFlag
                          - status
                        x-apifox-orders:
                          - username
                          - nickname
                          - headUrl
                          - signature
                          - followFlag
                          - followTime
                          - authInfo
                          - coverImgUrl
                          - spamStatus
                          - extFlag
                          - extInfo
                          - liveStatus
                          - liveCoverImgUrl
                          - liveInfo
                          - friendFollowCount
                          - oneTimeFlag
                          - status
                        description: 用户信息
                      feedsCount:
                        type: integer
                      continueFlag:
                        type: integer
                        description: 是否可以翻页 是:1
                      lastBuffer:
                        type: string
                        description: 翻页的标识，请求翻页时会用到
                      friendFollowCount:
                        type: integer
                        description: 好友关注数
                      userTags:
                        type: array
                        items:
                          type: string
                      preloadInfo:
                        type: object
                        properties:
                          preloadStrategyId:
                            type: integer
                          globalInfo:
                            type: object
                            properties:
                              prevCount:
                                type: integer
                              nextCount:
                                type: integer
                              maxBitRate:
                                type: integer
                              preloadFileMinBytes:
                                type: integer
                              preloadMaxConcurrentCount:
                                type: integer
                              megavideoMaxBitRate:
                                type: integer
                              megavideoPrevCount:
                                type: integer
                              megavideoNextCount:
                                type: integer
                              minBufferLength:
                                type: integer
                              maxBufferLength:
                                type: integer
                              minCurrentFeedBufferLength:
                                type: integer
                              canPreCreatedPlayer:
                                type: integer
                            required:
                              - prevCount
                              - nextCount
                              - maxBitRate
                              - preloadFileMinBytes
                              - preloadMaxConcurrentCount
                              - megavideoMaxBitRate
                              - megavideoPrevCount
                              - megavideoNextCount
                              - minBufferLength
                              - maxBufferLength
                              - minCurrentFeedBufferLength
                              - canPreCreatedPlayer
                            x-apifox-orders:
                              - prevCount
                              - nextCount
                              - maxBitRate
                              - preloadFileMinBytes
                              - preloadMaxConcurrentCount
                              - megavideoMaxBitRate
                              - megavideoPrevCount
                              - megavideoNextCount
                              - minBufferLength
                              - maxBufferLength
                              - minCurrentFeedBufferLength
                              - canPreCreatedPlayer
                        required:
                          - preloadStrategyId
                          - globalInfo
                        x-apifox-orders:
                          - preloadStrategyId
                          - globalInfo
                      privateLock:
                        type: integer
                      liveDurationHours:
                        type: integer
                      justWatch:
                        type: object
                        properties:
                          showJustWatch:
                            type: integer
                          allowPrefetch:
                            type: integer
                        required:
                          - showJustWatch
                          - allowPrefetch
                        x-apifox-orders:
                          - showJustWatch
                          - allowPrefetch
                      ipRegionInfo:
                        type: object
                        properties: {}
                        x-apifox-orders: []
                        description: 地区信息
                      mcnInfo:
                        type: object
                        properties:
                          agencyName:
                            type: string
                        required:
                          - agencyName
                        x-apifox-orders:
                          - agencyName
                      productInfo:
                        type: object
                        properties: {}
                        x-apifox-orders: []
                    required:
                      - object
                      - finderUserInfo
                      - contact
                      - feedsCount
                      - continueFlag
                      - lastBuffer
                      - friendFollowCount
                      - userTags
                      - preloadInfo
                      - privateLock
                      - liveDurationHours
                      - justWatch
                      - ipRegionInfo
                      - mcnInfo
                      - productInfo
                    x-apifox-orders:
                      - object
                      - finderUserInfo
                      - contact
                      - feedsCount
                      - continueFlag
                      - lastBuffer
                      - friendFollowCount
                      - userTags
                      - preloadInfo
                      - privateLock
                      - liveDurationHours
                      - justWatch
                      - ipRegionInfo
                      - mcnInfo
                      - productInfo
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
                  object:
                    - id: 14195037502970006000
                      nickname: 朝夕v
                      username: >-
                        v2_060000231003b20faec8c6e18f10c7d6c903ec3db0776955d3d97c6b329d6aa58693bcdb7ad1@finder
                      objectDesc:
                        description: ''
                        media:
                          - Url: >-
                              http://wxapp.tc.qq.com/251/20304/stodownload?encfilekey=oibeqyX228riaCwo9STVsGLPj9UYCicgttv57KAwaibwgt59R0ZvexpfcXpicuZgK9KrWFnqVIGCmmeEELsRrp14MS0oiaUOguD6XaicBEDD69qqNI2Qaa01Z17Yj56V9olerBgeGv5egDtHJ0&bizid=1023&dotrans=0&hy=SH&idx=1&m=82071545ea946d89af9ea5d6ad0fb576
                            ThumbUrl: >-
                              http://wxapp.tc.qq.com/251/20350/stodownload?encfilekey=oibeqyX228riaCwo9STVsGLPj9UYCicgttv1yP5Z57icAlHCbKIfJMyjc6w0oSrmEBrYXzewfFv2c6gkUHREmCrru0rTbTiaqV0Jvu83Sibd1JTfiaBTdCLQMjO8RQwlCjlC64lA3mHfKN3Jlc&bizid=1023&dotrans=0&hy=SH&idx=1&m=244c5c71db596838df691d372e7c0479&picformat=200
                            MediaType: 2
                            VideoPlayLen: 0
                            Width: 1440
                            Height: 1080
                            Md5Sum: ''
                            FileSize: 297437
                            Bitrate: 0
                            coverUrl: ''
                            decodeKey: '643903603'
                            urlToken: >-
                              &token=o3K9JoTic9IjlxQ7ZcBmNg99d64yE0iaNr9ibUshMby3RbC3S55C3Hn8FCYInskWC4FNbLxHicA07RQYcfeJotTxncQVFAH819FDZyjG91eVpuHDpZjfQbzFWg&ctsc=39
                            thumbUrlToken: >-
                              &token=oA9SZ4icv8ItLqUfGvSBYt3uicJNCowNeBxzcyJDJuvzSEPcApEhggxYLUUjdLRkEXWSWelC2YlMAaRWpIRcrszz3P7CMlXkl0EDxleLNMXEc&ctsc=1-39
                            codecInfo:
                              thumbScore: 12
                              hdimgScore: 45
                            fullThumbUrl: >-
                              http://wxapp.tc.qq.com/251/20350/stodownload?encfilekey=oibeqyX228riaCwo9STVsGLPj9UYCicgttv1yP5Z57icAlHCbKIfJMyjc6w0oSrmEBrYXzewfFv2c6gkUHREmCrru0rTbTiaqV0Jvu83Sibd1JTfiaBTdCLQMjO8RQwlCjlC64lA3mHfKN3Jlc&bizid=1023&dotrans=0&hy=SH&idx=1&m=244c5c71db596838df691d372e7c0479&picformat=200
                            fullThumbUrlToken: >-
                              &token=oA9SZ4icv8IuB4V9QD1iclZzd7bkGs06liadprp529FkMgf50YzrdTDPYP8CcicnnV7ib8r8KtXEm6ErKg2djq4Wfb9khgRu73cWZlkQz8UblA9U&ctsc=3-39
                            fullCoverUrl: ''
                            liveCoverImgs:
                              - ThumbUrl: >-
                                  http://wxapp.tc.qq.com/251/20350/stodownload?encfilekey=oibeqyX228riaCwo9STVsGLPj9UYCicgttv1yP5Z57icAlHCbKIfJMyjc6w0oSrmEBrYXzewfFv2c6gkUHREmCrru0rTbTiaqV0Jvu83Sibd1JTfiaBTdCLQMjO8RQwlCjlC64lA3mHfKN3Jlc&bizid=1023&dotrans=0&hy=SH&idx=1&m=244c5c71db596838df691d372e7c0479
                                FileSize: 297437
                                Width: 1440
                                Height: 1080
                                Bitrate: 0
                            cardShowStyle: 0
                            dynamicRangeType: 0
                            videoType: 1
                          - Url: >-
                              http://wxapp.tc.qq.com/251/20304/stodownload?encfilekey=oibeqyX228riaCwo9STVsGLPj9UYCicgttvz7tHiay7nNxvJB3XKPvEuUhSdvoK3GckSDiaPJOqZnNaaTZibPYATvktg1qWDEShg5s6g8h79a1udSLNEdrRAPXwgQ4gG3HIyWOyA83V0WqYj0&bizid=1023&dotrans=0&hy=SH&idx=1&m=857ad08a06915c8fd77810d3a0bf6245
                            ThumbUrl: >-
                              http://wxapp.tc.qq.com/251/20350/stodownload?encfilekey=oibeqyX228riaCwo9STVsGLPj9UYCicgttvXia4icia4dYpVyxxmEmnFnndXTLqaibmOPXM2xQ5csekZIDZMOnTahH4bYYL8CsP1Fiadia7hb3y2ianicOjI4wsw8LicoSsOf8DUkGWJNoNc5pDE1FA&bizid=1023&dotrans=0&hy=SH&idx=1&m=e57a332f673663e810b4a7da0bf1e78e&picformat=200
                            MediaType: 2
                            VideoPlayLen: 0
                            Width: 1440
                            Height: 1080
                            Md5Sum: ''
                            FileSize: 326887
                            Bitrate: 0
                            coverUrl: ''
                            decodeKey: '1905017814'
                            urlToken: >-
                              &token=Cvvj5Ix3eew5xyibexEnJ55FVTGEs1Lxv6c89RoAcw7oIKYPyjpZuJB4ib6TulJvqyjh1Ym6jOCN7JFUMpzPn8HaNV5yWhs7cx7Hian4oIl9b4zcQEPXrEPnzic9BXiaNbWf5&ctsc=39
                            thumbUrlToken: >-
                              &token=KkOFht0mCXlnPibsrvuAjOVtAkNKkibwQicafa6o9DItibBh2g7av2R2NCtQ4VuW5uw9ylHVJfXlIkicQKVxBZE4vf2mnsLmnatdIPibGOp8AH1fk&ctsc=1-39
                            codecInfo:
                              thumbScore: 12
                              hdimgScore: 45
                            fullThumbUrl: >-
                              http://wxapp.tc.qq.com/251/20350/stodownload?encfilekey=oibeqyX228riaCwo9STVsGLPj9UYCicgttvXia4icia4dYpVyxxmEmnFnndXTLqaibmOPXM2xQ5csekZIDZMOnTahH4bYYL8CsP1Fiadia7hb3y2ianicOjI4wsw8LicoSsOf8DUkGWJNoNc5pDE1FA&bizid=1023&dotrans=0&hy=SH&idx=1&m=e57a332f673663e810b4a7da0bf1e78e&picformat=200
                            fullThumbUrlToken: >-
                              &token=oA9SZ4icv8IsicIhqwckUgX3z1akDrOa54E2BuMEqbWTv9iagia41beMly3WN6gyBkSJ19MZYKLUZv7Pv7jG0FEibafeAZXMOhwTrIz6Qw7enlSw&ctsc=3-39
                            fullCoverUrl: ''
                            liveCoverImgs:
                              - ThumbUrl: >-
                                  http://wxapp.tc.qq.com/251/20350/stodownload?encfilekey=oibeqyX228riaCwo9STVsGLPj9UYCicgttvXia4icia4dYpVyxxmEmnFnndXTLqaibmOPXM2xQ5csekZIDZMOnTahH4bYYL8CsP1Fiadia7hb3y2ianicOjI4wsw8LicoSsOf8DUkGWJNoNc5pDE1FA&bizid=1023&dotrans=0&hy=SH&idx=1&m=e57a332f673663e810b4a7da0bf1e78e
                                FileSize: 326887
                                Width: 1440
                                Height: 1080
                                Bitrate: 0
                            cardShowStyle: 0
                            dynamicRangeType: 0
                            videoType: 1
                        mediaType: 2
                        location: {}
                        extReading: {}
                        imgFeedBgmInfo:
                          docId: ''
                          albumThumbUrl: ''
                          name: ''
                          artist: ''
                          albumName: ''
                          mediaStreamingUrl: ''
                        followPostInfo:
                          musicInfo:
                            docId: '342066328'
                            albumThumbUrl: >-
                              http://wx.y.gtimg.cn/music/photo_new/T002R500x500M000001kWuR62LAvku_1.jpg
                            name: monsters
                            artist: 苏天伦
                            albumName: ''
                            mediaStreamingUrl: >-
                              https://cover.qpic.cn/206/20302/stodownload?m=b8c992316fbfde34eadf7c76051035ee&filekey=30350201010421301f020200ce040253480410b8c992316fbfde34eadf7c76051035ee02030f703a040d00000004627466730000000131&hy=SH&storeid=323032323039323330353036323130303035363831663139613364666266356336386234306230303030303063653030303034663465&bizid=1023
                            miniappInfo: ''
                            webUrl: ''
                            floatThumbUrl: ''
                            chorusBegin: 0
                            docType: 0
                            songId: ''
                          groupId: '342066328'
                          hasBgm: 1
                        fromApp: {}
                        event: {}
                        mvInfo: {}
                        draftObjectId: 14195067577171968000
                        clientDraftExtInfo:
                          lbsFlagType: 0
                          videoMusicId: '342066328'
                        generalReportInfo: {}
                        posterLocation:
                          longitude: 116.642105
                          latitude: 34.687767
                          city: Xuzhou City
                        shortTitle:
                          - CgA=
                        originalInfoDesc: {}
                        finderNewlifeDesc: {}
                      createtime: 1692180335
                      likeList:
                        - >-
                          Cg56aGFuZ2NodWFuMjI4OBIJ5pyd5aSV44CCKAA6qQFodHRwczovL3d4LnFsb2dvLmNuL21taGVhZC92ZXJfMS9YUm8xMUtTMU9PQVIwMTFaNmI0T1hITkNVSGdaNkROOTd4UzRrVU5sdm1CbWlhUkNpYlliTFNRWHEyU0hic0kyakdhbWV5bEVaVzluYVdCYkUyRnVpY0xQOFNHZnFiVFZoTWRDdTJjSWh6SmtLU203QVJoaWJkcVhFN3lNR3liQWs1WFcvMTMySNCZs6wGqgEA
                      forwardCount: 1
                      contact:
                        username: >-
                          v2_060000231003b20faec8c6e18f10c7d6c903ec3db0776955d3d97c6b329d6aa58693bcdb7ad1@finder
                        nickname: 朝夕v
                        headUrl: >-
                          https://wx.qlogo.cn/finderhead/ver_1/TDibw5X5xTzpMW9D4GE0YnYUMqPAspF0AibTwhdSFWjyt2tZCMuLVon1PIT6aGulvzvlSZPkDcT06NB6D1eoLicYBKiaBCRDXZJSMEErIGQkQJ8/0
                        seq: 1
                        signature: 。。。
                        followFlag: 1
                        authInfo: {}
                        coverImgUrl: ''
                        spamStatus: 0
                        extFlag: 262156
                        extInfo:
                          country: CN
                          province: Jiangsu
                          city: Xuzhou
                          sex: 2
                        liveStatus: 2
                        liveCoverImgUrl: >-
                          http://wxapp.tc.qq.com/251/20350/stodownload?m=be88b1cb981aa72b3328ccbd22a58e0b&filekey=30340201010420301e020200fb040253480410be88b1cb981aa72b3328ccbd22a58e0b02022814040d00000004627466730000000132&hy=SH&storeid=5649443df0009b8a38399cc84000000fb00004f7e534815c008e0b08dc805c&dotrans=0&bizid=1023
                        liveInfo:
                          anchorStatusFlag: 133248
                          switchFlag: 53727
                          lotterySetting:
                            settingFlag: 0
                            attendType: 4
                        friendFollowCount: 2
                        oneTimeFlag: 2
                        status: 0
                      displayid: 14195037502970006000
                      likeCount: 2
                      commentCount: 5
                      deletetime: 0
                      friendLikeCount: 1
                      objectNonceId: '16628169456191691547_0_39_2_1_0'
                      objectStatus: 0
                      sendShareFavWording: ''
                      originalFlag: 0
                      secondaryShowFlag: 1
                      sessionBuffer: >-
                        eyJjdXJfbGlrZV9jb3VudCI6MiwiY3VyX2NvbW1lbnRfY291bnQiOjUsInJlY2FsbF90eXBlcyI6W10sImRlbGl2ZXJ5X3NjZW5lIjoyLCJkZWxpdmVyeV90aW1lIjoxNzA2MDg2ODE2LCJzZXRfY29uZGl0aW9uX2ZsYWciOjksImZyaWVuZF9jb21tZW50X2luZm8iOnsibGFzdF9mcmllbmRfdXNlcm5hbWUiOiJ6aGFuZ2NodWFuMjI4OCIsImxhc3RfZnJpZW5kX2xpa2VfdGltZSI6MTcwMzcyNjI4OH0sInRvdGFsX2ZyaWVuZF9saWtlX2NvdW50IjoxLCJyZWNhbGxfaW5kZXgiOltdLCJtZWRpYV90eXBlIjoyLCJjcmVhdGVfdGltZSI6MTY5MjE4MDMzNSwicmVjYWxsX2luZm8iOltdLCJvZmxhZyI6NDA5NzYsImlkYyI6MSwiZGV2aWNlX3R5cGVfaWQiOjEzLCJkZXZpY2VfcGxhdGZvcm0iOiJpUGFkMTMsNyIsImZlZWRfcG9zIjowLCJjbGllbnRfcmVwb3J0X2J1ZmYiOiJ7XCJpZl9zcGxpdF9zY3JlZW5faXBhZFwiOjAsXCJlbnRlclNvdXJjZUluZm9cIjpcIntcXFwiZmluZGVydXNlcm5hbWVcXFwiOlxcXCJcXFwiLFxcXCJmZWVkaWRcXFwiOlxcXCJcXFwifVwiLFwiZXh0cmFpbmZvXCI6XCJ7XFxuIFxcXCJyZWdjb3VudHJ5XFxcIiA6IFxcXCJDTlxcXCJcXG59XCIsXCJzZXNzaW9uSWRcIjpcIjEwMV8xNzA2MDg2ODA1NTE3IyQwXzE3MDYwODY3OTI4ODEjXCIsXCJqdW1wSWRcIjp7XCJ0cmFjZWlkXCI6XCJcIixcInNvdXJjZWlkXCI6XCJcIn19IiwiY29tbWVudF9zY2VuZSI6MzksIm9iamVjdF9pZCI6MTQxOTUwMzc1MDI5NzAwMDU4MjIsImZpbmRlcl91aW4iOjEzMTA0ODA0MjY5NDM3NzA5LCJnZW9oYXNoIjozMzc3Njk5NzIwNTI3ODcyLCJlbnRyYW5jZV9zY2VuZSI6MSwiY2FyZF90eXBlIjoxLCJleHB0X2ZsYWciOjMwMDY3Njk5LCJ1c2VyX21vZGVsX2ZsYWciOjgsImlzX2ZyaWVuZCI6dHJ1ZSwiY3R4X2lkIjoiMS0xLTIwLWJmNmEyNzQzYzhiNTM1ZjJlNmY2MzEyZjUwZjM3M2VjMTcwNjA4NjgxMDY0MyIsImFkX2ZsYWciOjQsImVyaWwiOltdLCJwZ2tleXMiOltdLCJzY2lkIjoiZmRiMjg0MGMtYmE5Ni0xMWVlLTg0MDAtZGI5NzlkZmJlZTYwIn0=
                      favCount: 2
                      urlValidTime: 172800
                      forwardStyle: 0
                      permissionFlag: 2147483648
                      attachmentList: {}
                      objectType: 0
                      followFeedCount: 17
                      verifyInfoBuf: >-
                        CrADD3QLRKZljCPO5dJ958TJct7WbHzU3lM4r1PJtQpm8vbngWNGW346SKEAwM8tRL25uHNJfTR0co1F4k76AQY1EDg2GyDaz4PGCeyfiSP5uN6xS0sdYGw+ln0TdVVk1/clsefJAGJscIYDcfTms18Dkw4D79zgBGq3luGMY1TGRcjkopsxRvvYKYwB995y3pZXK9DisP1v1jA5ecMrXKuJDI5qIe6O5SYUk+OY5WQtTRZwELDojU/SiuuZ9eZFf2IkWUGL5FHHBxHB7WX3JcoNPyi0zLHyCVdBBkPIebN/w2RwCbwSXLGO+tqg3XYIRD3PC7ALOU1Hum+jwtUczQIqkFTaQZ+q99DdpMv1yYi5D2zCWxni0r/IfjqvuFSoumfErCW5DMDgny4kRZ4lqRhw0d4EDCLEz4Daz3q+vTIAme8yoWk4O8Wvb8FKvZIjjtSYCkXJLl9feh5oPaFsp8mzLrYCcAze+Lwac+0+e0bJRCuNNXdaFl6WT9fQ9RXP2d1pANk9oxiXVm1ISuzT50O9mcbQBMqoFhRvyBX+j3bppA1lhR3wsjqNws4Bby4OM/KM
                      wxStatusRefCount: 0
                      adFlag: 4
                      tipsInfo: {}
                      internalFeedbackUrl: ''
                      ringtoneCount: 0
                      funcFlag: 288
                      playhistoryInfo: {}
                      flowCardRecommandReason: {}
                      ipRegionInfo: {}
                  finderUserInfo:
                    coverImgUrl: ''
                  contact:
                    username: >-
                      v2_060000231003b20faec8c6e18f10c7d6c903ec3db0776955d3d97c6b329d6aa58693bcdb7ad1@finder
                    nickname: 朝夕v
                    headUrl: >-
                      https://wx.qlogo.cn/finderhead/ver_1/TDibw5X5xTzpMW9D4GE0YnYUMqPAspF0AibTwhdSFWjyt2tZCMuLVon1PIT6aGulvzvlSZPkDcT06NB6D1eoLicYBKiaBCRDXZJSMEErIGQkQJ8/0
                    signature: 。。。
                    followFlag: 1
                    followTime: 1706086669
                    authInfo: {}
                    coverImgUrl: ''
                    spamStatus: 0
                    extFlag: 262156
                    extInfo:
                      country: CN
                      province: Jiangsu
                      city: Xuzhou
                      sex: 2
                    liveStatus: 2
                    liveCoverImgUrl: >-
                      http://wxapp.tc.qq.com/251/20350/stodownload?m=be88b1cb981aa72b3328ccbd22a58e0b&filekey=30340201010420301e020200fb040253480410be88b1cb981aa72b3328ccbd22a58e0b02022814040d00000004627466730000000132&hy=SH&storeid=5649443df0009b8a38399cc84000000fb00004f7e534815c008e0b08dc805c&dotrans=0&bizid=1023
                    liveInfo:
                      anchorStatusFlag: 133248
                      switchFlag: 53727
                      lotterySetting:
                        settingFlag: 0
                        attendType: 4
                    friendFollowCount: 2
                    oneTimeFlag: 2
                    status: 0
                  feedsCount: 1
                  continueFlag: 0
                  lastBuffer: CL6SgI/o7Ln/xAEQARgAIL6SgI/o7Ln/xAE=
                  friendFollowCount: 2
                  userTags:
                    - 5aWz
                    - 5rGf6IuPIOW+kOW3ng==
                  preloadInfo:
                    preloadStrategyId: 4292783945
                    globalInfo:
                      prevCount: 0
                      nextCount: 4
                      maxBitRate: 250
                      preloadFileMinBytes: 0
                      preloadMaxConcurrentCount: 1
                      megavideoMaxBitRate: 250
                      megavideoPrevCount: 1
                      megavideoNextCount: 2
                      minBufferLength: 10
                      maxBufferLength: 20
                      minCurrentFeedBufferLength: 5
                      canPreCreatedPlayer: 0
                  privateLock: 0
                  liveDurationHours: 0
                  justWatch:
                    showJustWatch: 0
                    allowPrefetch: 0
                  ipRegionInfo: {}
                  mcnInfo:
                    agencyName: 江苏
                  productInfo: {}
          headers: {}
          x-apifox-name: 成功
      security: []
      x-apifox-folder: 基础API/视频号模块
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3475559/apis/api-144570567-run
components:
  schemas: {}
  securitySchemes: {}
servers:
  - url: http://218.78.116.24:10883
    description: 测试环境
security: []

```

# 关注列表

## OpenAPI

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /gewe/v2/api/finder/followList:
    post:
      summary: 关注列表
      deprecated: false
      description: ''
      tags:
        - 基础API/视频号模块
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
                myUserName:
                  type: string
                  description: 自己的username
                myRoleType:
                  type: integer
                  description: 自己的roletype
                lastBuffer:
                  type: string
                  description: 首次传空，后续传接口返回的lastBuffer
              required:
                - appId
                - myUserName
                - myRoleType
              x-apifox-orders:
                - appId
                - myUserName
                - myRoleType
                - lastBuffer
            example:
              appId: '{{appid}}'
              proxyIp: ''
              myUserName: >-
                v2_060000231003b20faec8c7e28811c4d5cc0ded37b0779c48c759a7446a87688c2774e5300c32@finder
              lastBuffer: ''
              myRoleType: 3
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
                      contactList:
                        type: array
                        items:
                          type: object
                          properties:
                            username:
                              type: string
                              description: 关注人的username
                            nickname:
                              type: string
                              description: 昵称
                            headUrl:
                              type: string
                              description: 头像
                            signature:
                              type: string
                              description: 简介
                            followFlag:
                              type: integer
                            followTime:
                              type: integer
                              description: 关注时间
                            authInfo:
                              type: object
                              properties: {}
                              x-apifox-orders: []
                            coverImgUrl:
                              type: string
                            spamStatus:
                              type: integer
                            extFlag:
                              type: integer
                            extInfo:
                              type: object
                              properties:
                                sex:
                                  type: integer
                                  description: 性别
                                country:
                                  type: string
                                  description: 国家
                                province:
                                  type: string
                                  description: 省份
                                city:
                                  type: string
                                  description: 城市
                              required:
                                - country
                                - province
                                - city
                                - sex
                              x-apifox-orders:
                                - sex
                                - country
                                - province
                                - city
                              description: 扩展信息
                            liveStatus:
                              type: integer
                            liveCoverImgUrl:
                              type: string
                            liveInfo:
                              type: object
                              properties:
                                anchorStatusFlag:
                                  type: integer
                                switchFlag:
                                  type: integer
                                lotterySetting:
                                  type: object
                                  properties:
                                    settingFlag:
                                      type: integer
                                    attendType:
                                      type: integer
                                  required:
                                    - settingFlag
                                    - attendType
                                  x-apifox-orders:
                                    - settingFlag
                                    - attendType
                              required:
                                - anchorStatusFlag
                                - switchFlag
                                - lotterySetting
                              x-apifox-orders:
                                - anchorStatusFlag
                                - switchFlag
                                - lotterySetting
                            status:
                              type: integer
                          required:
                            - username
                            - nickname
                            - headUrl
                            - signature
                            - followFlag
                            - followTime
                            - authInfo
                            - coverImgUrl
                            - spamStatus
                            - extFlag
                            - extInfo
                            - liveStatus
                            - liveCoverImgUrl
                            - liveInfo
                            - status
                          x-apifox-orders:
                            - username
                            - nickname
                            - headUrl
                            - signature
                            - followFlag
                            - followTime
                            - authInfo
                            - coverImgUrl
                            - spamStatus
                            - extFlag
                            - extInfo
                            - liveStatus
                            - liveCoverImgUrl
                            - liveInfo
                            - status
                      lastBuffer:
                        type: string
                        description: 翻页标识，对应请求参数中的lastBuffer
                      continueFlag:
                        type: integer
                        description: 是否可以翻页，是：1 否：0
                      followCount:
                        type: integer
                        description: 关注总数
                    required:
                      - contactList
                      - lastBuffer
                      - continueFlag
                      - followCount
                    x-apifox-orders:
                      - contactList
                      - lastBuffer
                      - continueFlag
                      - followCount
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
                  contactList:
                    - username: >-
                        v2_060000231003b20faec8c7e28811c4d5cc0ded37b0779c48c759a7446a87688c2774e5300c32@finder
                      nickname: 未来可期啊哈
                      headUrl: >-
                        https://wx.qlogo.cn/finderhead/ver_1/D5kOMSrTOprOibFVZ2NOO8AnohFdlDMhoNTZr1C8D9d5K6og92mcc3lxDEFcQldBibqjzIx2iavenQO0TMzhjmrUibmn3iaoaLYtNiaGFWjZgCd5t92shsicTvcyiaIjFjRtwVgy/0
                      signature: 理智，清醒，知进退。
                      followFlag: 1
                      followTime: 1706090194
                      authInfo: {}
                      coverImgUrl: ''
                      spamStatus: 0
                      extFlag: 262152
                      extInfo:
                        sex: 1
                      liveStatus: 2
                      liveCoverImgUrl: ''
                      liveInfo:
                        anchorStatusFlag: 2048
                        switchFlag: 53727
                        lotterySetting:
                          settingFlag: 0
                          attendType: 4
                      status: 0
                    - username: >-
                        v2_060000231003b20faec8c6e18f10c7d6c903ec3db0776955d3d97c6b329d6aa58693bcdb7ad1@finder
                      nickname: 朝夕v
                      headUrl: >-
                        https://wx.qlogo.cn/finderhead/ver_1/TDibw5X5xTzpMW9D4GE0YnYUMqPAspF0AibTwhdSFWjyt2tZCMuLVon1PIT6aGulvzvlSZPkDcT06NB6D1eoLicYBKiaBCRDXZJSMEErIGQkQJ8/0
                      signature: 。。。
                      followFlag: 1
                      followTime: 1706086669
                      authInfo: {}
                      coverImgUrl: ''
                      spamStatus: 0
                      extFlag: 262156
                      extInfo:
                        country: CN
                        province: Jiangsu
                        city: Xuzhou
                        sex: 2
                      liveStatus: 2
                      liveCoverImgUrl: >-
                        http://wxapp.tc.qq.com/251/20350/stodownload?m=be88b1cb981aa72b3328ccbd22a58e0b&filekey=30340201010420301e020200fb040253480410be88b1cb981aa72b3328ccbd22a58e0b02022814040d00000004627466730000000132&hy=SH&storeid=5649443df0009b8a38399cc84000000fb00004f7e534815c008e0b08dc805c&dotrans=0&bizid=1023
                      liveInfo:
                        anchorStatusFlag: 133248
                        switchFlag: 53727
                        lotterySetting:
                          settingFlag: 0
                          attendType: 4
                      status: 0
                  lastBuffer: COMF
                  continueFlag: 0
                  followCount: 2
          headers: {}
          x-apifox-name: 成功
      security: []
      x-apifox-folder: 基础API/视频号模块
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3475559/apis/api-144597891-run
components:
  schemas: {}
  securitySchemes: {}
servers:
  - url: http://218.78.116.24:10883
    description: 测试环境
security: []

```

# 消息列表

## OpenAPI

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /gewe/v2/api/finder/mentionList:
    post:
      summary: 消息列表
      deprecated: false
      description: ''
      tags:
        - 基础API/视频号模块
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
                myUserName:
                  type: string
                  description: 自己的username
                myRoleType:
                  type: integer
                  description: 自己的roletype
                reqScene:
                  type: integer
                  description: 消息类型    3是点赞 4是评论 5是关注
                lastBuff:
                  type: string
                  description: 首次传空，后续传接口返回的lastBuffer
              required:
                - appId
                - myUserName
                - lastBuff
                - myRoleType
                - reqScene
              x-apifox-orders:
                - appId
                - myUserName
                - myRoleType
                - lastBuff
                - reqScene
            example:
              appId: '{{appid}}'
              myUserName: '{{userName}}'
              lastBuff: ''
              myRoleType: 3
              reqScene: 4
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
                      list:
                        type: object
                        properties:
                          mentions:
                            type: array
                            items:
                              type: object
                              properties:
                                headUrl:
                                  type: string
                                  description: 头像
                                nickname:
                                  type: string
                                  description: 昵称
                                mentionType:
                                  type: integer
                                  description: '消息类型  7:点赞  '
                                mentionContent:
                                  type: string
                                  description: 消息内容
                                createtime:
                                  type: integer
                                  description: 时间
                                thumbUrl:
                                  type: string
                                  description: 缩略图
                                mentionId:
                                  type: integer
                                  description: 消息ID
                                refObjectId:
                                  type: integer
                                  description: 引用的作品ID
                                refCommentId:
                                  type: integer
                                  description: 引用的评论ID
                                flag:
                                  type: integer
                                extflag:
                                  type: integer
                                refContent:
                                  type: string
                                mediaType:
                                  type: integer
                                description:
                                  type: string
                                  description: 描述
                                replyNickname:
                                  type: string
                                refObjectNonceId:
                                  type: string
                                username:
                                  type: string
                                  description: 对方的username/微信ID
                                contact:
                                  type: object
                                  properties:
                                    contact:
                                      type: object
                                      properties:
                                        username:
                                          type: string
                                          description: username
                                        nickname:
                                          type: string
                                          description: 昵称
                                        headUrl:
                                          type: string
                                          description: 头像
                                        seq:
                                          type: integer
                                        signature:
                                          type: string
                                          description: 简介
                                        authInfo:
                                          type: object
                                          properties: {}
                                          x-apifox-orders: []
                                        coverImgUrl:
                                          type: string
                                        spamStatus:
                                          type: integer
                                        extFlag:
                                          type: integer
                                        extInfo:
                                          type: object
                                          properties:
                                            country:
                                              type: string
                                              description: 国家
                                            province:
                                              type: string
                                              description: 省份
                                            city:
                                              type: string
                                              description: 城市
                                            sex:
                                              type: integer
                                              description: 性别
                                          required:
                                            - country
                                            - province
                                            - city
                                            - sex
                                          x-apifox-orders:
                                            - country
                                            - province
                                            - city
                                            - sex
                                        liveStatus:
                                          type: integer
                                        liveCoverImgUrl:
                                          type: string
                                        liveInfo:
                                          type: object
                                          properties:
                                            anchorStatusFlag:
                                              type: integer
                                            switchFlag:
                                              type: integer
                                            lotterySetting:
                                              type: object
                                              properties:
                                                settingFlag:
                                                  type: integer
                                                attendType:
                                                  type: integer
                                              required:
                                                - settingFlag
                                                - attendType
                                              x-apifox-orders:
                                                - settingFlag
                                                - attendType
                                          required:
                                            - anchorStatusFlag
                                            - switchFlag
                                            - lotterySetting
                                          x-apifox-orders:
                                            - anchorStatusFlag
                                            - switchFlag
                                            - lotterySetting
                                        status:
                                          type: integer
                                      required:
                                        - username
                                        - nickname
                                        - headUrl
                                        - seq
                                        - signature
                                        - authInfo
                                        - coverImgUrl
                                        - spamStatus
                                        - extFlag
                                        - extInfo
                                        - liveStatus
                                        - liveCoverImgUrl
                                        - liveInfo
                                        - status
                                      x-apifox-orders:
                                        - username
                                        - nickname
                                        - headUrl
                                        - seq
                                        - signature
                                        - authInfo
                                        - coverImgUrl
                                        - spamStatus
                                        - extFlag
                                        - extInfo
                                        - liveStatus
                                        - liveCoverImgUrl
                                        - liveInfo
                                        - status
                                  required:
                                    - contact
                                  x-apifox-orders:
                                    - contact
                                refObjectType:
                                  type: integer
                                extInfo:
                                  type: object
                                  properties:
                                    appName:
                                      type: string
                                    entityId:
                                      type: string
                                  required:
                                    - appName
                                    - entityId
                                  x-apifox-orders:
                                    - appName
                                    - entityId
                                svrMentionId:
                                  type: integer
                                followFlag:
                                  type: integer
                                orderCount:
                                  type: integer
                                interactionCount:
                                  type: integer
                                forceUseRefContent:
                                  type: integer
                              x-apifox-orders:
                                - headUrl
                                - nickname
                                - mentionType
                                - mentionContent
                                - createtime
                                - thumbUrl
                                - mentionId
                                - refObjectId
                                - refCommentId
                                - flag
                                - extflag
                                - refContent
                                - mediaType
                                - description
                                - replyNickname
                                - refObjectNonceId
                                - username
                                - contact
                                - refObjectType
                                - extInfo
                                - svrMentionId
                                - followFlag
                                - orderCount
                                - interactionCount
                                - forceUseRefContent
                        required:
                          - mentions
                        x-apifox-orders:
                          - mentions
                      lastBuff:
                        type: string
                        description: 翻页标识，对应请求参数中的lastBuffer
                    required:
                      - list
                      - lastBuff
                    x-apifox-orders:
                      - list
                      - lastBuff
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
                  list:
                    mentions:
                      - headUrl: >-
                          http://wx.qlogo.cn/finderhead/ajNVdqHZLLBn2wux0rkD6gc4NLsC0zqSeWeJNnp1bGnnPCHl0tt56A/0
                        nickname: 我的生活选择
                        mentionType: 18
                        mentionContent: 谢谢你的关注
                        createtime: 1699863094
                        thumbUrl: ''
                        mentionId: 268435463
                        refObjectId: 140674547237424
                        refCommentId: 0
                        flag: 0
                        extflag: 3
                        refContent: ''
                        mediaType: 0
                        description: ''
                        replyNickname: ''
                        refObjectNonceId: ''
                        username: >-
                          v2_060000231003b20faec8c7e58d1dcad6ce0ced33b0773abe5958d674168d77f7102844347047@finder
                        contact:
                          contact:
                            username: >-
                              v2_060000231003b20faec8c7e58d1dcad6ce0ced33b0773abe5958d674168d77f7102844347047@finder
                            nickname: 我的生活选择
                            headUrl: >-
                              https://wx.qlogo.cn/finderhead/ver_1/qOI5dkUOJ8YodCzzxP9ibztL9XrEbTeq0qJSXXeWribxs0eJicNBHOOLtJOAKpltTyboILgerib13g2tbQfws6QFiajvcvKD935KeibMcVYeguegA/0
                            seq: 57
                            signature: 追求自己想要的生活，努力前进，让自己变的更好
                            authInfo: {}
                            coverImgUrl: ''
                            spamStatus: 0
                            extFlag: 262156
                            extInfo:
                              country: CN
                              province: Hunan
                              city: Shaoyang
                              sex: 2
                            liveStatus: 2
                            liveCoverImgUrl: ''
                            liveInfo:
                              anchorStatusFlag: 2048
                              switchFlag: 53727
                              lotterySetting:
                                settingFlag: 0
                                attendType: 4
                            status: 0
                        refObjectType: 0
                        extInfo:
                          appName: ''
                          entityId: ''
                        svrMentionId: 8
                        followFlag: 0
                        orderCount: 0
                        interactionCount: 0
                        forceUseRefContent: 0
                  lastBuff: CAgQABj///9/
          headers: {}
          x-apifox-name: 成功
      security: []
      x-apifox-folder: 基础API/视频号模块
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3475559/apis/api-144598053-run
components:
  schemas: {}
  securitySchemes: {}
servers:
  - url: http://218.78.116.24:10883
    description: 测试环境
security: []

```

# 评论列表

## OpenAPI

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /gewe/v2/api/finder/commentList:
    post:
      summary: 评论列表
      deprecated: false
      description: ''
      tags:
        - 基础API/视频号模块
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
                objectId:
                  type: integer
                  description: 视频号ID
                lastBuffer:
                  type: string
                  description: 首次传空，后续传接口返回的lastBuffer
                sessionBuffer:
                  type: string
                  description: 视频号的sessionBuffer
                objectNonceId:
                  type: string
                  description: 视频号的objectNonceId
                refCommentId:
                  type: integer
                  description: 获取评论回复时传
                rootCommentId:
                  type: integer
                  description: 获取评论回复时传
              required:
                - appId
                - sessionBuffer
                - objectId
              x-apifox-orders:
                - appId
                - objectId
                - lastBuffer
                - sessionBuffer
                - objectNonceId
                - refCommentId
                - rootCommentId
            example:
              appId: '{{appid}}'
              proxyIp: ''
              rootCommentId: 0
              refCommentId: 0
              objectNonceId: '16628169456191691547_0_39_2_1_0'
              sessionBuffer: >-
                eyJjdXJfbGlrZV9jb3VudCI6MiwiY3VyX2NvbW1lbnRfY291bnQiOjUsInJlY2FsbF90eXBlcyI6W10sImRlbGl2ZXJ5X3NjZW5lIjoyLCJkZWxpdmVyeV90aW1lIjoxNzA2MDg2ODE2LCJzZXRfY29uZGl0aW9uX2ZsYWciOjksImZyaWVuZF9jb21tZW50X2luZm8iOnsibGFzdF9mcmllbmRfdXNlcm5hbWUiOiJ6aGFuZ2NodWFuMjI4OCIsImxhc3RfZnJpZW5kX2xpa2VfdGltZSI6MTcwMzcyNjI4OH0sInRvdGFsX2ZyaWVuZF9saWtlX2NvdW50IjoxLCJyZWNhbGxfaW5kZXgiOltdLCJtZWRpYV90eXBlIjoyLCJjcmVhdGVfdGltZSI6MTY5MjE4MDMzNSwicmVjYWxsX2luZm8iOltdLCJvZmxhZyI6NDA5NzYsImlkYyI6MSwiZGV2aWNlX3R5cGVfaWQiOjEzLCJkZXZpY2VfcGxhdGZvcm0iOiJpUGFkMTMsNyIsImZlZWRfcG9zIjowLCJjbGllbnRfcmVwb3J0X2J1ZmYiOiJ7XCJpZl9zcGxpdF9zY3JlZW5faXBhZFwiOjAsXCJlbnRlclNvdXJjZUluZm9cIjpcIntcXFwiZmluZGVydXNlcm5hbWVcXFwiOlxcXCJcXFwiLFxcXCJmZWVkaWRcXFwiOlxcXCJcXFwifVwiLFwiZXh0cmFpbmZvXCI6XCJ7XFxuIFxcXCJyZWdjb3VudHJ5XFxcIiA6IFxcXCJDTlxcXCJcXG59XCIsXCJzZXNzaW9uSWRcIjpcIjEwMV8xNzA2MDg2ODA1NTE3IyQwXzE3MDYwODY3OTI4ODEjXCIsXCJqdW1wSWRcIjp7XCJ0cmFjZWlkXCI6XCJcIixcInNvdXJjZWlkXCI6XCJcIn19IiwiY29tbWVudF9zY2VuZSI6MzksIm9iamVjdF9pZCI6MTQxOTUwMzc1MDI5NzAwMDU4MjIsImZpbmRlcl91aW4iOjEzMTA0ODA0MjY5NDM3NzA5LCJnZW9oYXNoIjozMzc3Njk5NzIwNTI3ODcyLCJlbnRyYW5jZV9zY2VuZSI6MSwiY2FyZF90eXBlIjoxLCJleHB0X2ZsYWciOjMwMDY3Njk5LCJ1c2VyX21vZGVsX2ZsYWciOjgsImlzX2ZyaWVuZCI6dHJ1ZSwiY3R4X2lkIjoiMS0xLTIwLWJmNmEyNzQzYzhiNTM1ZjJlNmY2MzEyZjUwZjM3M2VjMTcwNjA4NjgxMDY0MyIsImFkX2ZsYWciOjQsImVyaWwiOltdLCJwZ2tleXMiOltdLCJzY2lkIjoiZmRiMjg0MGMtYmE5Ni0xMWVlLTg0MDAtZGI5NzlkZmJlZTYwIn0=
              lastBuffer: CL6SgI/o7Ln/xAEQARgAIL6SgI/o7Ln/xAE=
              objectId: 14195037502970006000
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
                      lastBuffer:
                        type: string
                        description: 翻页标识，请求翻页时会用到
                      commentInfo:
                        type: array
                        items:
                          type: object
                          properties:
                            username:
                              type: string
                              description: 评论人的username
                            nickname:
                              type: string
                              description: 昵称
                            content:
                              type: string
                              description: 评论内容
                            commentId:
                              type: integer
                              description: 评论的ID
                            replyCommentId:
                              type: integer
                              description: 回复评论的ID
                            headUrl:
                              type: string
                              description: 头像
                            createtime:
                              type: integer
                              description: 评论时间
                            likeFlag:
                              type: integer
                            likeCount:
                              type: integer
                              description: 点赞数
                            expandCommentCount:
                              type: integer
                              description: 展开的评论数
                            continueFlag:
                              type: integer
                            displayFlag:
                              type: integer
                            replyContent:
                              type: string
                              description: 回复评论内容
                            upContinueFlag:
                              type: integer
                            extFlag:
                              type: integer
                            authorContact:
                              type: object
                              properties:
                                username:
                                  type: string
                                nickname:
                                  type: string
                                headUrl:
                                  type: string
                              required:
                                - username
                                - nickname
                                - headUrl
                              x-apifox-orders:
                                - username
                                - nickname
                                - headUrl
                            contentType:
                              type: integer
                              description: 评论类型
                            reportJson:
                              type: string
                            ipRegionInfo:
                              type: object
                              properties:
                                regionText:
                                  type: array
                                  items:
                                    type: string
                              required:
                                - regionText
                              x-apifox-orders:
                                - regionText
                              description: 地区信息
                            levelTwoComment:
                              type: array
                              items:
                                type: string
                          required:
                            - username
                            - nickname
                            - content
                            - commentId
                            - replyCommentId
                            - headUrl
                            - createtime
                            - likeFlag
                            - likeCount
                            - expandCommentCount
                            - continueFlag
                            - displayFlag
                            - replyContent
                            - upContinueFlag
                            - authorContact
                            - contentType
                            - reportJson
                            - ipRegionInfo
                          x-apifox-orders:
                            - username
                            - nickname
                            - content
                            - commentId
                            - replyCommentId
                            - headUrl
                            - createtime
                            - likeFlag
                            - likeCount
                            - expandCommentCount
                            - continueFlag
                            - displayFlag
                            - replyContent
                            - upContinueFlag
                            - extFlag
                            - authorContact
                            - contentType
                            - reportJson
                            - ipRegionInfo
                            - levelTwoComment
                      countInfo:
                        type: object
                        properties:
                          commentCount:
                            type: integer
                            description: 评论数
                          likeCount:
                            type: integer
                            description: 点赞数
                          forwardCount:
                            type: integer
                            description: 转发数
                          favCount:
                            type: integer
                            description: 收藏数
                        required:
                          - commentCount
                          - likeCount
                          - forwardCount
                          - favCount
                        x-apifox-orders:
                          - commentCount
                          - likeCount
                          - forwardCount
                          - favCount
                      upContinueFlag:
                        type: integer
                      downContinueFlag:
                        type: integer
                      monotonicData:
                        type: object
                        properties:
                          countInfo:
                            type: object
                            properties:
                              commentCount:
                                type: integer
                              likeCount:
                                type: integer
                              forwardCount:
                                type: integer
                              favCount:
                                type: integer
                            required:
                              - commentCount
                              - likeCount
                              - forwardCount
                              - favCount
                            x-apifox-orders:
                              - commentCount
                              - likeCount
                              - forwardCount
                              - favCount
                          commentCount:
                            type: object
                            properties:
                              commentCount:
                                type: integer
                            required:
                              - commentCount
                            x-apifox-orders:
                              - commentCount
                        required:
                          - countInfo
                          - commentCount
                        x-apifox-orders:
                          - countInfo
                          - commentCount
                    required:
                      - commentInfo
                      - countInfo
                      - lastBuffer
                      - upContinueFlag
                      - downContinueFlag
                      - monotonicData
                    x-apifox-orders:
                      - lastBuffer
                      - commentInfo
                      - countInfo
                      - upContinueFlag
                      - downContinueFlag
                      - monotonicData
                required:
                  - ret
                  - msg
                  - data
                x-apifox-orders:
                  - ret
                  - msg
                  - data
              example: "{\n    \"ret\": 200,\n    \"msg\": \"操作成功\",\n    \"data\": {\n        \"commentInfo\": [\n            {\n                \"username\": \"v2_060000231003b20faec8c6e18f10c7d6c903ec3db0776955d3d97c6b329d6aa58693bcdb7ad1@finder\",\n                \"nickname\": \"朝夕v\",\n                \"content\": \"。。\",\n                \"commentId\": 14305741204655704125,\n                \"replyCommentId\": 0,\n                \"headUrl\": \"http://wx.qlogo.cn/finderhead/Q3auHgzwzM5grqOsJtnHiaiapZ4cv43GNBTMaIUC7mVSGhKAPVyfY17w/0\",\n                \"createtime\": 1705377245,\n                \"likeFlag\": 0,\n                \"likeCount\": 0,\n                \"expandCommentCount\": 0,\n                \"continueFlag\": 0,\n                \"displayFlag\": 2,\n                \"replyContent\": \"\",\n                \"upContinueFlag\": 0,\n                \"extFlag\": 2,\n                \"authorContact\": {\n                    \"username\": \"v2_060000231003b20faec8c6e18f10c7d6c903ec3db0776955d3d97c6b329d6aa58693bcdb7ad1@finder\",\n                    \"nickname\": \"朝夕v\",\n                    \"headUrl\": \"http://wx.qlogo.cn/finderhead/Q3auHgzwzM5grqOsJtnHiaiapZ4cv43GNBTMaIUC7mVSGhKAPVyfY17w/0\"\n                },\n                \"contentType\": 0,\n                \"reportJson\": \"{}\",\n                \"ipRegionInfo\": {\n                    \"regionText\": [\n                        \"江苏\"\n                    ]\n                }\n            },\n            {\n                \"username\": \"v5_020b0a166104010000000000ed5c075b5fe340000000b1afa7d8728e3dd43ef4317a780e33c2de646dc7a8e59366e1f748ba6d9fc09714e897e44b9e9b517892fc49168b6e38b5c0352e519c26c4f368f3fd37@stranger\",\n                \"nickname\": \"朝夕。\",\n                \"content\": \"评论内容\",\n                \"commentId\": 14305150019061090364,\n                \"replyCommentId\": 0,\n                \"headUrl\": \"https://wx.qlogo.cn/mmhead/ver_1/lkib5XsC6ia74xkuskSe7o96KCtBOCO9lfrtufGn3pFwWclDxhj9enH2YVSUuRKr1zgBBPSndactfvicqURxzhePRIJnlBCPrfyXt3mnHqbrcrOeBH4jlDHwLDL9LRoyKJA/132\",\n                \"createtime\": 1705306770,\n                \"likeFlag\": 0,\n                \"likeCount\": 0,\n                \"expandCommentCount\": 0,\n                \"continueFlag\": 0,\n                \"displayFlag\": 0,\n                \"replyContent\": \"\",\n                \"upContinueFlag\": 0,\n                \"authorContact\": {\n                    \"username\": \"v5_020b0a166104010000000000ed5c075b5fe340000000b1afa7d8728e3dd43ef4317a780e33c2de646dc7a8e59366e1f748ba6d9fc09714e897e44b9e9b517892fc49168b6e38b5c0352e519c26c4f368f3fd37@stranger\",\n                    \"nickname\": \"朝夕。\",\n                    \"headUrl\": \"https://wx.qlogo.cn/mmhead/ver_1/lkib5XsC6ia74xkuskSe7o96KCtBOCO9lfrtufGn3pFwWclDxhj9enH2YVSUuRKr1zgBBPSndactfvicqURxzhePRIJnlBCPrfyXt3mnHqbrcrOeBH4jlDHwLDL9LRoyKJA/132\"\n                },\n                \"contentType\": 0,\n                \"reportJson\": \"{}\",\n                \"ipRegionInfo\": {\n                    \"regionText\": [\n                        \"浙江\"\n                    ]\n                }\n            },\n            {\n                \"username\": \"v5_020b0a166104010000000000ed5c075b5fe340000000b1afa7d8728e3dd43ef4317a780e33c2de646dc7a8e59366e1f748ba6d9fc09714e897e44b9e9b517892fc49168b6e38b5c0352e519c26c4f368f3fd37@stranger\",\n                \"nickname\": \"朝夕。\",\n                \"content\": \"hh\",\n                \"commentId\": 14305098373537073222,\n                \"replyCommentId\": 0,\n                \"headUrl\": \"https://wx.qlogo.cn/mmhead/ver_1/lkib5XsC6ia74xkuskSe7o96KCtBOCO9lfrtufGn3pFwWclDxhj9enH2YVSUuRKr1zgBBPSndactfvicqURxzhePRIJnlBCPrfyXt3mnHqbrcrOeBH4jlDHwLDL9LRoyKJA/132\",\n                \"createtime\": 1705300614,\n                \"likeFlag\": 0,\n                \"likeCount\": 0,\n                \"expandCommentCount\": 0,\n                \"continueFlag\": 0,\n                \"displayFlag\": 0,\n                \"replyContent\": \"\",\n                \"upContinueFlag\": 0,\n                \"authorContact\": {\n                    \"username\": \"v5_020b0a166104010000000000ed5c075b5fe340000000b1afa7d8728e3dd43ef4317a780e33c2de646dc7a8e59366e1f748ba6d9fc09714e897e44b9e9b517892fc49168b6e38b5c0352e519c26c4f368f3fd37@stranger\",\n                    \"nickname\": \"朝夕。\",\n                    \"headUrl\": \"https://wx.qlogo.cn/mmhead/ver_1/lkib5XsC6ia74xkuskSe7o96KCtBOCO9lfrtufGn3pFwWclDxhj9enH2YVSUuRKr1zgBBPSndactfvicqURxzhePRIJnlBCPrfyXt3mnHqbrcrOeBH4jlDHwLDL9LRoyKJA/132\"\n                },\n                \"contentType\": 0,\n                \"reportJson\": \"{}\",\n                \"ipRegionInfo\": {\n                    \"regionText\": [\n                        \"浙江\"\n                    ]\n                }\n            },\n            {\n                \"username\": \"v2_060000231003b20faec8c7ea8f1ecbd1c901ef3cb0773696efb506324185fdd53ba44426a8a7@finder\",\n                \"nickname\": \"阿星5679\",\n                \"content\": \"哈哈\",\n                \"commentId\": 14279589493825607865,\n                \"replyCommentId\": 0,\n                \"headUrl\": \"http://wx.qlogo.cn/finderhead/SQd7RF5caa0TmEbngQTrcibuK8MmrARRSDKxbNrMWiaX7NcuABsSSTUA/0\",\n                \"levelTwoComment\": [\"\\nVv2_060000231003b20faec8c6e18f10c7d6c903ec3db0776955d3d97c6b329d6aa58693bcdb7ad1@finder\x12\a朝夕v\x1A\\b/::D/::D ������ҕ�\x01(������ҕ�\x01:Xhttp://wx.qlogo.cn/finderhead/Q3auHgzwzM5grqOsJtnHiaiapZ4cv43GNBTMaIUC7mVSGhKAPVyfY17w/0H��٫\x06`\0h\0�\x01\x02�\x01\x06哈哈�\x01\x02�\x01�\x01\\nVv2_060000231003b20faec8c6e18f10c7d6c903ec3db0776955d3d97c6b329d6aa58693bcdb7ad1@finder\x12\a朝夕v\x1AXhttp://wx.qlogo.cn/finderhead/Q3auHgzwzM5grqOsJtnHiaiapZ4cv43GNBTMaIUC7mVSGhKAPVyfY17w/0�\x01\0�\x02\x02{}�\x02\\b\\n\x06江苏\"\n                ],\n                \"createtime\": 1702259718,\n                \"likeFlag\": 0,\n                \"likeCount\": 0,\n                \"expandCommentCount\": 1,\n                \"continueFlag\": 0,\n                \"displayFlag\": 520,\n                \"replyContent\": \"\",\n                \"upContinueFlag\": 0,\n                \"authorContact\": {\n                    \"username\": \"v2_060000231003b20faec8c7ea8f1ecbd1c901ef3cb0773696efb506324185fdd53ba44426a8a7@finder\",\n                    \"nickname\": \"阿星5679\",\n                    \"headUrl\": \"http://wx.qlogo.cn/finderhead/SQd7RF5caa0TmEbngQTrcibuK8MmrARRSDKxbNrMWiaX7NcuABsSSTUA/0\"\n                },\n                \"contentType\": 0,\n                \"reportJson\": \"{}\",\n                \"ipRegionInfo\": {\n                    \"regionText\": [\n                        \"江苏\"\n                    ]\n                }\n            }\n        ],\n        \"countInfo\": {\n            \"commentCount\": 5,\n            \"likeCount\": 2,\n            \"forwardCount\": 1,\n            \"favCount\": 2\n        },\n        \"lastBuffer\": \"CgsIubGAr8/f0pXGARABCL6SgI/o7Ln/xAEYACC+koCP6Oy5/8QB\",\n        \"upContinueFlag\": 0,\n        \"downContinueFlag\": 0,\n        \"monotonicData\": {\n            \"countInfo\": {\n                \"commentCount\": 5,\n                \"likeCount\": 2,\n                \"forwardCount\": 1,\n                \"favCount\": 2\n            },\n            \"commentCount\": {\n                \"commentCount\": 5\n            }\n        }\n    }\n}"
          headers: {}
          x-apifox-name: 成功
      security: []
      x-apifox-folder: 基础API/视频号模块
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3475559/apis/api-144571885-run
components:
  schemas: {}
  securitySchemes: {}
servers:
  - url: http://218.78.116.24:10883
    description: 测试环境
security: []

```

# 获取赞与收藏的视频列表

## OpenAPI

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /gewe/v2/api/finder/likeFavList:
    post:
      summary: 获取赞与收藏的视频列表
      deprecated: false
      description: ''
      tags:
        - 基础API/视频号模块
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
                myUserName:
                  type: string
                  description: 自己的username
                myRoleType:
                  type: integer
                  description: 自己的roletype
                lastBuffer:
                  type: string
                  description: 首次传空，后续传接口返回的lastBuffer
                flag:
                  type: integer
                  description: 7是全部 1是红心 2是大拇指 4是收藏
              required:
                - appId
                - myUserName
                - myRoleType
                - flag
              x-apifox-orders:
                - appId
                - myUserName
                - myRoleType
                - lastBuffer
                - flag
            example:
              appId: '{{appid}}'
              proxyIp: ''
              myUserName: >-
                v2_060000231003b20faec8c7e28811c4d5cc0ded37b0779c48c759a7446a87688c2774e5300c32@finder
              lastBuffer: ''
              myRoleType: 3
              flag: 7
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
                      object:
                        type: array
                        items:
                          type: object
                          properties:
                            id:
                              type: integer
                            nickname:
                              type: string
                            username:
                              type: string
                            objectDesc:
                              type: object
                              properties:
                                description:
                                  type: string
                                media:
                                  type: array
                                  items:
                                    type: object
                                    properties:
                                      Url:
                                        type: string
                                      ThumbUrl:
                                        type: string
                                      MediaType:
                                        type: integer
                                      VideoPlayLen:
                                        type: integer
                                      Width:
                                        type: integer
                                      Height:
                                        type: integer
                                      Md5Sum:
                                        type: string
                                      FileSize:
                                        type: integer
                                      Bitrate:
                                        type: integer
                                      Spec:
                                        type: array
                                        items:
                                          type: object
                                          properties:
                                            fileFormat:
                                              type: string
                                            firstLoadBytes:
                                              type: integer
                                            bitRate:
                                              type: integer
                                            codingFormat:
                                              type: string
                                          required:
                                            - fileFormat
                                            - firstLoadBytes
                                            - bitRate
                                            - codingFormat
                                          x-apifox-orders:
                                            - fileFormat
                                            - firstLoadBytes
                                            - bitRate
                                            - codingFormat
                                      coverUrl:
                                        type: string
                                      decodeKey:
                                        type: string
                                      urlToken:
                                        type: string
                                      thumbUrlToken:
                                        type: string
                                      coverUrlToken:
                                        type: string
                                      codecInfo:
                                        type: object
                                        properties:
                                          videoScore:
                                            type: integer
                                          videoCoverScore:
                                            type: integer
                                          videoAudioScore:
                                            type: integer
                                          thumbScore:
                                            type: integer
                                          hdimgScore:
                                            type: integer
                                          hasStickers:
                                            type: integer
                                          useAlgorithmCover:
                                            type: integer
                                        required:
                                          - videoScore
                                          - videoCoverScore
                                          - videoAudioScore
                                          - thumbScore
                                          - hdimgScore
                                          - hasStickers
                                          - useAlgorithmCover
                                        x-apifox-orders:
                                          - videoScore
                                          - videoCoverScore
                                          - videoAudioScore
                                          - thumbScore
                                          - hdimgScore
                                          - hasStickers
                                          - useAlgorithmCover
                                      hotFlag:
                                        type: integer
                                      fullThumbUrl:
                                        type: string
                                      fullThumbUrlToken:
                                        type: string
                                      fullCoverUrl:
                                        type: string
                                      liveCoverImgs:
                                        type: array
                                        items:
                                          type: object
                                          properties:
                                            ThumbUrl:
                                              type: string
                                            FileSize:
                                              type: integer
                                            Width:
                                              type: integer
                                            Height:
                                              type: integer
                                            Bitrate:
                                              type: integer
                                          x-apifox-orders:
                                            - ThumbUrl
                                            - FileSize
                                            - Width
                                            - Height
                                            - Bitrate
                                      scalingInfo:
                                        type: object
                                        properties:
                                          version:
                                            type: string
                                          isSplitScreen:
                                            type: boolean
                                          upPercentPosition:
                                            type: integer
                                          downPercentPosition:
                                            type: integer
                                        required:
                                          - version
                                          - isSplitScreen
                                          - upPercentPosition
                                          - downPercentPosition
                                        x-apifox-orders:
                                          - version
                                          - isSplitScreen
                                          - upPercentPosition
                                          - downPercentPosition
                                      cardShowStyle:
                                        type: integer
                                      dynamicRangeType:
                                        type: integer
                                      videoType:
                                        type: integer
                                    x-apifox-orders:
                                      - Url
                                      - ThumbUrl
                                      - MediaType
                                      - VideoPlayLen
                                      - Width
                                      - Height
                                      - Md5Sum
                                      - FileSize
                                      - Bitrate
                                      - Spec
                                      - coverUrl
                                      - decodeKey
                                      - urlToken
                                      - thumbUrlToken
                                      - coverUrlToken
                                      - codecInfo
                                      - hotFlag
                                      - fullThumbUrl
                                      - fullThumbUrlToken
                                      - fullCoverUrl
                                      - liveCoverImgs
                                      - scalingInfo
                                      - cardShowStyle
                                      - dynamicRangeType
                                      - videoType
                                mediaType:
                                  type: integer
                                location:
                                  type: object
                                  properties:
                                    longitude:
                                      type: number
                                    latitude:
                                      type: number
                                    city:
                                      type: string
                                    poiName:
                                      type: string
                                    poiAddress:
                                      type: string
                                    poiClassifyId:
                                      type: string
                                    poiClassifyType:
                                      type: integer
                                  required:
                                    - longitude
                                    - latitude
                                    - city
                                    - poiName
                                    - poiAddress
                                    - poiClassifyId
                                    - poiClassifyType
                                  x-apifox-orders:
                                    - longitude
                                    - latitude
                                    - city
                                    - poiName
                                    - poiAddress
                                    - poiClassifyId
                                    - poiClassifyType
                                extReading:
                                  type: object
                                  properties: {}
                                  x-apifox-orders: []
                                topic:
                                  type: object
                                  properties: {}
                                  x-apifox-orders: []
                                imgFeedBgmInfo:
                                  type: object
                                  properties:
                                    docId:
                                      type: string
                                    albumThumbUrl:
                                      type: string
                                    name:
                                      type: string
                                    artist:
                                      type: string
                                    albumName:
                                      type: string
                                    mediaStreamingUrl:
                                      type: string
                                  required:
                                    - docId
                                    - albumThumbUrl
                                    - name
                                    - artist
                                    - albumName
                                    - mediaStreamingUrl
                                  x-apifox-orders:
                                    - docId
                                    - albumThumbUrl
                                    - name
                                    - artist
                                    - albumName
                                    - mediaStreamingUrl
                                followPostInfo:
                                  type: object
                                  properties:
                                    musicInfo:
                                      type: object
                                      properties:
                                        docId:
                                          type: string
                                        albumThumbUrl:
                                          type: string
                                        name:
                                          type: string
                                        artist:
                                          type: string
                                        albumName:
                                          type: string
                                        mediaStreamingUrl:
                                          type: string
                                        miniappInfo:
                                          type: string
                                        webUrl:
                                          type: string
                                        floatThumbUrl:
                                          type: string
                                        chorusBegin:
                                          type: integer
                                        docType:
                                          type: integer
                                        songId:
                                          type: string
                                      required:
                                        - docId
                                        - albumThumbUrl
                                        - name
                                        - artist
                                        - albumName
                                        - mediaStreamingUrl
                                        - miniappInfo
                                        - webUrl
                                        - floatThumbUrl
                                        - chorusBegin
                                        - docType
                                        - songId
                                      x-apifox-orders:
                                        - docId
                                        - albumThumbUrl
                                        - name
                                        - artist
                                        - albumName
                                        - mediaStreamingUrl
                                        - miniappInfo
                                        - webUrl
                                        - floatThumbUrl
                                        - chorusBegin
                                        - docType
                                        - songId
                                    groupId:
                                      type: string
                                    hasBgm:
                                      type: integer
                                  required:
                                    - musicInfo
                                    - groupId
                                    - hasBgm
                                  x-apifox-orders:
                                    - musicInfo
                                    - groupId
                                    - hasBgm
                                fromApp:
                                  type: object
                                  properties: {}
                                  x-apifox-orders: []
                                event:
                                  type: object
                                  properties: {}
                                  x-apifox-orders: []
                                mvInfo:
                                  type: object
                                  properties: {}
                                  x-apifox-orders: []
                                draftObjectId:
                                  type: integer
                                clientDraftExtInfo:
                                  type: object
                                  properties:
                                    lbsFlagType:
                                      type: integer
                                    videoMusicId:
                                      type: string
                                  required:
                                    - lbsFlagType
                                    - videoMusicId
                                  x-apifox-orders:
                                    - lbsFlagType
                                    - videoMusicId
                                generalReportInfo:
                                  type: object
                                  properties: {}
                                  x-apifox-orders: []
                                posterLocation:
                                  type: object
                                  properties:
                                    longitude:
                                      type: number
                                    latitude:
                                      type: number
                                    city:
                                      type: string
                                  required:
                                    - longitude
                                    - latitude
                                    - city
                                  x-apifox-orders:
                                    - longitude
                                    - latitude
                                    - city
                                shortTitle:
                                  type: array
                                  items:
                                    type: string
                                originalInfoDesc:
                                  type: object
                                  properties:
                                    type:
                                      type: integer
                                  required:
                                    - type
                                  x-apifox-orders:
                                    - type
                                finderNewlifeDesc:
                                  type: object
                                  properties: {}
                                  x-apifox-orders: []
                              required:
                                - description
                                - media
                                - mediaType
                                - location
                                - extReading
                                - topic
                                - imgFeedBgmInfo
                                - followPostInfo
                                - fromApp
                                - event
                                - mvInfo
                                - draftObjectId
                                - clientDraftExtInfo
                                - generalReportInfo
                                - posterLocation
                                - shortTitle
                                - originalInfoDesc
                                - finderNewlifeDesc
                              x-apifox-orders:
                                - description
                                - media
                                - mediaType
                                - location
                                - extReading
                                - topic
                                - imgFeedBgmInfo
                                - followPostInfo
                                - fromApp
                                - event
                                - mvInfo
                                - draftObjectId
                                - clientDraftExtInfo
                                - generalReportInfo
                                - posterLocation
                                - shortTitle
                                - originalInfoDesc
                                - finderNewlifeDesc
                            createtime:
                              type: integer
                            likeFlag:
                              type: integer
                            likeList:
                              type: array
                              items:
                                type: string
                            forwardCount:
                              type: integer
                            contact:
                              type: object
                              properties:
                                username:
                                  type: string
                                nickname:
                                  type: string
                                headUrl:
                                  type: string
                                seq:
                                  type: integer
                                signature:
                                  type: string
                                authInfo:
                                  type: object
                                  properties:
                                    authIconType:
                                      type: integer
                                    authProfession:
                                      type: string
                                    detailLink:
                                      type: string
                                    appName:
                                      type: string
                                  required:
                                    - authIconType
                                    - authProfession
                                    - detailLink
                                    - appName
                                  x-apifox-orders:
                                    - authIconType
                                    - authProfession
                                    - detailLink
                                    - appName
                                coverImgUrl:
                                  type: string
                                spamStatus:
                                  type: integer
                                extFlag:
                                  type: integer
                                extInfo:
                                  type: object
                                  properties:
                                    country:
                                      type: string
                                    province:
                                      type: string
                                    city:
                                      type: string
                                    sex:
                                      type: integer
                                  required:
                                    - country
                                    - province
                                    - city
                                    - sex
                                  x-apifox-orders:
                                    - country
                                    - province
                                    - city
                                    - sex
                                liveStatus:
                                  type: integer
                                liveCoverImgUrl:
                                  type: string
                                liveInfo:
                                  type: object
                                  properties:
                                    anchorStatusFlag:
                                      type: integer
                                    switchFlag:
                                      type: integer
                                    micSetting:
                                      type: object
                                      properties: {}
                                      x-apifox-orders: []
                                    lotterySetting:
                                      type: object
                                      properties:
                                        settingFlag:
                                          type: integer
                                        attendType:
                                          type: integer
                                      required:
                                        - settingFlag
                                        - attendType
                                      x-apifox-orders:
                                        - settingFlag
                                        - attendType
                                  required:
                                    - anchorStatusFlag
                                    - switchFlag
                                    - micSetting
                                    - lotterySetting
                                  x-apifox-orders:
                                    - anchorStatusFlag
                                    - switchFlag
                                    - micSetting
                                    - lotterySetting
                                friendFollowCount:
                                  type: integer
                                status:
                                  type: integer
                                clubInfo:
                                  type: object
                                  properties: {}
                                  x-apifox-orders: []
                              required:
                                - username
                                - nickname
                                - headUrl
                                - seq
                                - signature
                                - authInfo
                                - coverImgUrl
                                - spamStatus
                                - extFlag
                                - extInfo
                                - liveStatus
                                - liveCoverImgUrl
                                - liveInfo
                                - friendFollowCount
                                - status
                                - clubInfo
                              x-apifox-orders:
                                - username
                                - nickname
                                - headUrl
                                - seq
                                - signature
                                - authInfo
                                - coverImgUrl
                                - spamStatus
                                - extFlag
                                - extInfo
                                - liveStatus
                                - liveCoverImgUrl
                                - liveInfo
                                - friendFollowCount
                                - status
                                - clubInfo
                            likeCount:
                              type: integer
                            commentCount:
                              type: integer
                            deletetime:
                              type: integer
                            friendLikeCount:
                              type: integer
                            objectNonceId:
                              type: string
                            objectStatus:
                              type: integer
                            sendShareFavWording:
                              type: string
                            originalFlag:
                              type: integer
                            secondaryShowFlag:
                              type: integer
                            sessionBuffer:
                              type: string
                            favCount:
                              type: integer
                            urlValidTime:
                              type: integer
                            forwardStyle:
                              type: integer
                            permissionFlag:
                              type: integer
                            attachmentList:
                              type: object
                              properties: {}
                              x-apifox-orders: []
                            objectType:
                              type: integer
                            followFeedCount:
                              type: integer
                            verifyInfoBuf:
                              type: string
                            wxStatusRefCount:
                              type: integer
                            adFlag:
                              type: integer
                            internalFeedbackUrl:
                              type: string
                            ringtoneCount:
                              type: integer
                            funcFlag:
                              type: integer
                            playhistoryInfo:
                              type: object
                              properties: {}
                              x-apifox-orders: []
                            finderPromotionJumpinfo:
                              type: object
                              properties: {}
                              x-apifox-orders: []
                            flowCardRecommandReason:
                              type: object
                              properties: {}
                              x-apifox-orders: []
                            ipRegionInfo:
                              type: object
                              properties: {}
                              x-apifox-orders: []
                          x-apifox-orders:
                            - id
                            - nickname
                            - username
                            - objectDesc
                            - createtime
                            - likeFlag
                            - likeList
                            - forwardCount
                            - contact
                            - likeCount
                            - commentCount
                            - deletetime
                            - friendLikeCount
                            - objectNonceId
                            - objectStatus
                            - sendShareFavWording
                            - originalFlag
                            - secondaryShowFlag
                            - sessionBuffer
                            - favCount
                            - urlValidTime
                            - forwardStyle
                            - permissionFlag
                            - attachmentList
                            - objectType
                            - followFeedCount
                            - verifyInfoBuf
                            - wxStatusRefCount
                            - adFlag
                            - internalFeedbackUrl
                            - ringtoneCount
                            - funcFlag
                            - playhistoryInfo
                            - finderPromotionJumpinfo
                            - flowCardRecommandReason
                            - ipRegionInfo
                        description: 列表信息
                      continueFlag:
                        type: integer
                        description: 是否可以翻页，是：1 否：0
                      lastBuffer:
                        type: string
                        description: 翻页标识，对应请求参数中的lastBuffer
                    required:
                      - object
                      - continueFlag
                      - lastBuffer
                    x-apifox-orders:
                      - lastBuffer
                      - continueFlag
                      - object
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
                  object:
                    - id: 14171058819644721000
                      nickname: 吉恩.山里人家
                      username: >-
                        v2_060000231003b20faec8c5eb811ec7dcce05ed34b0779b64782e6da639203e8b68d9affe31e8@finder
                      objectDesc:
                        description: 鳝蛋：传统食谱！#记录农村生活
                        media:
                          - Url: >-
                              http://wxapp.tc.qq.com/251/20302/stodownload?encfilekey=6xykWLEnztKcKCJZcV0rWCM8ua7DibZkibqXGfPxf5lrricuy1sEams3IW5yAhibhFrRn7wiakyrmZ9fERETHuEhIBoREcvaj1WUxIqWvN7MTjxx9CeVeWj3P1w6ibIMtqdMvcxuveBw6vcf6wIsibI0nuadZTPb66tEjzCbNQlXCYRlbE&a=1&bizid=1023&dotrans=0&hy=SH&idx=1&m=0cbd64b42198a9b9c002d79f58459df3
                            ThumbUrl: >-
                              http://wxapp.tc.qq.com/251/20350/stodownload?encfilekey=Cvvj5Ix3eexKX1zo1IZZBrQomawdVfSQH1uu2U31EqGhndX0MYXo8vRI0l4OBMKxct9I4Y1QOUZ4iaia5JgjhWENwRxBVLLHH8xU2wCMrxHLU96puPFcPA1FxYb6rkdvMFLh8JMoJ1vH600CkbHXe6AibWqPArwtBoCqBITrUiborRQ&bizid=1023&dotrans=0&hy=SH&idx=1&m=7567fed1a48f3e7aacc2559184c536ba
                            MediaType: 4
                            VideoPlayLen: 31
                            Width: 1080
                            Height: 1920
                            Md5Sum: 5b09e9cfe3d1a627697a77ccce7cf10e
                            FileSize: 59782986
                            Bitrate: 14796
                            Spec:
                              - fileFormat: xWT111
                                firstLoadBytes: 1701871
                                bitRate: 281
                                codingFormat: h264
                              - fileFormat: xWT112
                                firstLoadBytes: 1253490
                                bitRate: 211
                                codingFormat: h264
                              - fileFormat: xWT113
                                firstLoadBytes: 834227
                                bitRate: 146
                                codingFormat: h264
                              - fileFormat: xWT156
                                firstLoadBytes: 913698
                                bitRate: 143
                                codingFormat: h265
                              - fileFormat: xWT157
                                firstLoadBytes: 726268
                                bitRate: 117
                                codingFormat: h265
                              - fileFormat: xWT158
                                firstLoadBytes: 596509
                                bitRate: 96
                                codingFormat: h265
                            coverUrl: >-
                              http://wxapp.tc.qq.com/251/20304/stodownload?encfilekey=oibeqyX228riaCwo9STVsGLPj9UYCicgttv1z0q5rdqkUY6iaaiavseSHm0qHJcomtib9ABHiaOp4foNd1m8LoMbZQjY1ibBmZZ7yqcafudqCzibDVZuC6ZXjNVXiaf9KmRryKIgTLe6QiaBfOcicxE&bizid=1023&dotrans=0&hy=SH&idx=1&m=caecfef30fda533fe7917347bb63cf9a
                            decodeKey: '277374214'
                            urlToken: >-
                              &token=o3K9JoTic9IhLnPdVqra6n3Dkpf0Pxks14ueFX1DkF5N0NCT0GjJEyk1nH0IicYkicVfOXWVeeIvJicUAia7x67Jj6xjjPX5EYAx7psWacIHk52Ik49j2Fa3qQQ&extg=10f3000&svrbypass=AAuL%2FQsFAAABAAAAAADfPzdK6Xyx1dBr5Rl0ZhAAAADnaHZTnGbFfAj9RgZXfw6VQy%2B8tutQ3riJfyny1FedwEDpH0ybW23rMV3oYQwzc3WOh%2BJPx1Pznog%3D&svrnonce=1718884837
                            thumbUrlToken: >-
                              &token=oA9SZ4icv8Ivx3kCzcPQJTf51ZGHYSohuYic0wURd2POdsODZzQN54Ot9lAiaicf8DnbBhYpGqTdmVbApR1XCgRtFDhBJF7v08toO6z2BiazX120
                            coverUrlToken: >-
                              &token=oA9SZ4icv8IvVqvXOWR3tibpCfe93QqXmDebjKkRgaNl0POvAyugfibro136ar0UtJicfgXs5nZwtbcqjfuYsZEXzicujFfkmzkNFJryyTSArLgc
                            codecInfo:
                              videoScore: 0
                              videoCoverScore: 0
                              videoAudioScore: 0
                              thumbScore: 0
                              hdimgScore: 0
                              hasStickers: 0
                              useAlgorithmCover: 0
                            hotFlag: 1
                            fullThumbUrl: >-
                              http://wxapp.tc.qq.com/251/20350/stodownload?encfilekey=Cvvj5Ix3eexKX1zo1IZZBrQomawdVfSQH1uu2U31EqGhndX0MYXo8vRI0l4OBMKxct9I4Y1QOUZ4iaia5JgjhWENwRxBVLLHH8xU2wCMrxHLU96puPFcPA1FxYb6rkdvMFLh8JMoJ1vH600CkbHXe6AibWqPArwtBoCqBITrUiborRQ&bizid=1023&dotrans=0&hy=SH&idx=1&m=7567fed1a48f3e7aacc2559184c536ba
                            fullThumbUrlToken: >-
                              &token=KkOFht0mCXnBB37p5h9DIibtrh07AGs2YQB0icrTjacmSHuBgh3ac6HyNiaYiaj9UuQdMgZDhjvcHprPasNj00hXEgFDCBg5ibTwUcia4BSHRCcJc
                            fullCoverUrl: >-
                              http://wxapp.tc.qq.com/251/20350/stodownload?m=7f04140486ddce9e757d3f6bbc084e38&filekey=30350201010421301f020200fb0402534804107f04140486ddce9e757d3f6bbc084e38020302a1a4040d00000004627466730000000132&hy=SH&storeid=564b1017d0009ab24b279d589000000fb00004f7e534822d458e0b11a6dcd4&dotrans=0&bizid=1023
                            liveCoverImgs:
                              - ThumbUrl: >-
                                  http://wxapp.tc.qq.com/251/20350/stodownload?bizid=1023&dotrans=0&encfilekey=Cvvj5Ix3eexKX1zo1IZZBrQomawdVfSQH1uu2U31EqGhndX0MYXo8vRI0l4OBMKxct9I4Y1QOUZ4iaia5JgjhWENwRxBVLLHH8xU2wCMrxHLU96puPFcPA1FxYb6rkdvMFLh8JMoJ1vH600CkbHXe6AibWqPArwtBoCqBITrUiborRQ&hy=SH&idx=1&m=7567fed1a48f3e7aacc2559184c536ba&token=6xykWLEnztJl9hwrgv8vtb9icH7CDeFLUiaWHUCOK81PKYlWxQqrSSxicW00TmmTFbkBMfeFw33UckoP8LRNrsRuw
                                FileSize: 59782986
                                Width: 1080
                                Height: 1920
                                Bitrate: 0
                            scalingInfo:
                              version: v2.0.1
                              isSplitScreen: false
                              upPercentPosition: 0
                              downPercentPosition: 0
                            cardShowStyle: 0
                            dynamicRangeType: 0
                            videoType: 2
                        mediaType: 4
                        location:
                          longitude: 109.108734
                          latitude: 25.914429
                          city: 黔东南苗族侗族自治州
                          poiName: ''
                          poiAddress: ''
                          poiClassifyId: ''
                          poiClassifyType: 1
                        extReading: {}
                        topic: {}
                        imgFeedBgmInfo:
                          docId: ''
                          albumThumbUrl: ''
                          name: ''
                          artist: ''
                          albumName: ''
                          mediaStreamingUrl: ''
                        followPostInfo:
                          musicInfo:
                            docId: ''
                            albumThumbUrl: ''
                            name: ''
                            artist: ''
                            albumName: ''
                            mediaStreamingUrl: ''
                            miniappInfo: ''
                            webUrl: ''
                            floatThumbUrl: ''
                            chorusBegin: 0
                            docType: 0
                            songId: ''
                          groupId: ''
                          hasBgm: 1
                        fromApp: {}
                        event: {}
                        mvInfo: {}
                        draftObjectId: 14171088724426752000
                        clientDraftExtInfo:
                          lbsFlagType: 2
                          videoMusicId: '0'
                        generalReportInfo: {}
                        posterLocation:
                          longitude: 109.10884
                          latitude: 25.914791
                          city: Qiandongnanmiaozudongzu AutonomousPrefecture
                        shortTitle:
                          - CgA=
                        originalInfoDesc:
                          type: 24
                        finderNewlifeDesc: {}
                      createtime: 1689321854
                      likeFlag: 1
                      likeList:
                        - >-
                          ChN3eGlkXzd0bXc3M3IyaHBqcTIyEgblvrfljY4oADqSAWh0dHBzOi8vd3gucWxvZ28uY24vbW1oZWFkL3Zlcl8xLzdZN25FS1JEelRGcERMc1ZyMTJIbGxLaWFwbnZQN0JydDVuOXdGTVREazRpY3VzMW15bXdlM290UEFSRDk4TjlYYW9KU2tyRkJMSXNPejcxdDhwVFdFRDB1YWtjUWZmZHFGS0h5M2V4UVd4Q2svMTMySLPw/6sGqgEA
                      forwardCount: 96100
                      contact:
                        username: >-
                          v2_060000231003b20faec8c5eb811ec7dcce05ed34b0779b64782e6da639203e8b68d9affe31e8@finder
                        nickname: 吉恩.山里人家
                        headUrl: >-
                          https://wx.qlogo.cn/finderhead/ver_1/xZxQHAuwZQUMQNS5Ar7wFPafmL8CdBv6QtjibUotVia8xyq1k2ZpZqUdGYDpiaL8TQRUJ1MZia5ne7KdWp7wfTsERicxLJtVoMUYhKRS2yRgiatAM/0
                        seq: 1
                        signature: >-
                          请备注来意：u15888188

                          很多人会问“吉恩”会的东西咋那么多？只因受家中老人影响，儿时常常跟随老人巡山间、识百草，学习古书，便爱上博大精深的传统文化，也希望在平台上能认识更多志同道合的朋友！
                        authInfo:
                          authIconType: 1
                          authProfession: 美食博主
                          detailLink: >-
                            pages/index/index.html?showdetail=true&username=v2_060000231003b20faec8c5eb811ec7dcce05ed34b0779b64782e6da639203e8b68d9affe31e8@finder
                          appName: gh_4ee148a6ecaa@app
                        coverImgUrl: ''
                        spamStatus: 0
                        extFlag: 2359564
                        extInfo:
                          country: CN
                          province: Guizhou
                          city: Southeast
                          sex: 1
                        liveStatus: 2
                        liveCoverImgUrl: ''
                        liveInfo:
                          anchorStatusFlag: 2048
                          switchFlag: 53727
                          micSetting: {}
                          lotterySetting:
                            settingFlag: 0
                            attendType: 4
                        friendFollowCount: 0
                        status: 0
                        clubInfo: {}
                      likeCount: 100002
                      commentCount: 15290
                      deletetime: 0
                      friendLikeCount: 1
                      objectNonceId: '16516030573457893333_0_0_124_1_0'
                      objectStatus: 0
                      sendShareFavWording: ''
                      originalFlag: 0
                      secondaryShowFlag: 1
                      sessionBuffer: >-
                        eyJjdXJfbGlrZV9jb3VudCI6MzA5MTI2LCJjdXJfY29tbWVudF9jb3VudCI6MTUyOTAsInJlY2FsbF90eXBlcyI6W10sImRlbGl2ZXJ5X3NjZW5lIjoxMjQsImRlbGl2ZXJ5X3RpbWUiOjE3MTg4ODQ4MzgsImZyaWVuZF9jb21tZW50X2luZm8iOnsibGFzdF9mcmllbmRfdXNlcm5hbWUiOiJ3eGlkXzd0bXc3M3IyaHBqcTIyIiwibGFzdF9mcmllbmRfbGlrZV90aW1lIjoxNzAyODg1NDI3fSwidG90YWxfZnJpZW5kX2xpa2VfY291bnQiOjEsInJlY2FsbF9pbmRleCI6W10sIm1lZGlhX3R5cGUiOjQsInZpZF9sZW4iOjMxLCJjcmVhdGVfdGltZSI6MTY4OTMyMTg1NCwicmVjYWxsX2luZm8iOltdLCJpZGMiOjMsImRldmljZV90eXBlX2lkIjoxMywiZGV2aWNlX3BsYXRmb3JtIjoiaVBhZDExLDMiLCJmZWVkX3BvcyI6MCwiY2xpZW50X3JlcG9ydF9idWZmIjoie1wiaWZfc3BsaXRfc2NyZWVuX2lwYWRcIjowLFwiZW50ZXJTb3VyY2VJbmZvXCI6XCJ7XFxcImZpbmRlcnVzZXJuYW1lXFxcIjpcXFwiXFxcIixcXFwiZmVlZGlkXFxcIjpcXFwiXFxcIn1cIixcImV4dHJhaW5mb1wiOlwie1xcXCJyZWdjb3VudHJ5XFxcIjpcXFwiQ05cXFwiO1xcXCJpc19waXBfZW50ZXJcXFwiOjA7XFxcInRpcHNfdXVpZFxcXCI6XFxcIlxcXCI7XFxcInBpcF9lbnRlcl90eXBlXFxcIjowfVwiLFwic2Vzc2lvbklkXCI6XCIxNDNfMTcxODg4NDc4MzMxMyMkMl8xNzE4ODg0NzgzNDMxI1wiLFwianVtcElkXCI6e1widHJhY2VpZFwiOlwiXCIsXCJzb3VyY2VpZFwiOlwiXCJ9fSIsIm9iamVjdF9pZCI6MTQxNzEwNTg4MTk2NDQ3MjEyODgsImZpbmRlcl91aW4iOjEzMTA0ODA3ODg3NDkwMTEwLCJjaXR5Ijoi6buU5Lic5Y2X6IuX5peP5L6X5peP6Ieq5rK75beeIiwiZ2VvaGFzaCI6NDAyMzYyOTAyMTQ5NjQ5MiwiZW50cmFuY2Vfc2NlbmUiOjEsImNhcmRfdHlwZSI6MSwiZXhwdF9mbGFnIjo4ODc4Nzk1NSwiY3R4X2lkIjoiMS0xLTIwLTkwYjQxYzI0MThmMjU5NmRjOGM2NjU4MmUwMDNiNGExMTcxODg4NDc4MzU2MyIsImFkX2ZsYWciOjQsIm9ial9mbGFnIjoxNjM4NDAsImVyaWwiOltdLCJwZ2tleXMiOltdLCJvYmpfZXh0X2ZsYWciOjE3MTM3ODU2LCJzY2lkIjoiYjRmYTlkYWEtMmVmYy0xMWVmLWI1ZmMtZmJiNjJkNTY1MWQ2In0=
                      favCount: 100002
                      urlValidTime: 172800
                      forwardStyle: 0
                      permissionFlag: 2148532224
                      attachmentList: {}
                      objectType: 0
                      followFeedCount: 17
                      verifyInfoBuf: >-
                        CsADo4Keaf+NZGunSbnN/+2u4/uy751B7rq991MU/zRwTDmo5hgPIuoIY9PZAdWqytF5quILy3/d+7LJ7CtqGNrKrpQVYqXvU9pprkJOlAw9jVcIP70+D2yoVDnomoLec5fvtrpD7QkYNlClknNU1mEML/LxilEqvBfGaS2/BN1QDUNIt3qkQeCgQdxSGDa4O2wcd5KBlqxyUyf3JX0inXrfsqZGAGtxYyS5QKzF0tFR57wQzqqxR1XNVuxo26kEqpIrrLPO1QnlUfAUVI5uRvl57waS5mcxTV4N0zHDBeklUjozsaUhCqWiTqg1svgRWlNILjAZkJhDjqJIvA4j+7hQ52V4AqR89W50p1EVOLRoyeQjJPtWwviXUtFp5Ds1ERGtFq07hx6vcTgu24wVS/EvSv6erV52wt7QW48+CyVpkmZ9px5z9H6xnwOtTKRkwUR2L1whsoFU1F1tlIpiywIjtKyjj2eaie4DRgXgM+TaZcvTdTg/BL6VmLAHDpYvSXl6sTOT60eyqoW020Tg1nN4eQww/jsO4vVM7asRUpWC9vZFK5hJDgTIQKLlPV/TrLYh4VcLZsgupWByyouzf+J8RQ==
                      wxStatusRefCount: 184
                      adFlag: 4
                      internalFeedbackUrl: ''
                      ringtoneCount: 903
                      funcFlag: 384
                      playhistoryInfo: {}
                      finderPromotionJumpinfo: {}
                      flowCardRecommandReason: {}
                      ipRegionInfo: {}
                  continueFlag: 0
                  lastBuffer: CLPw/6sGEAFY/////w9gAagB/////w+wAQH4Af////8PgAIB
          headers: {}
          x-apifox-name: 成功
      security: []
      x-apifox-folder: 基础API/视频号模块
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3475559/apis/api-186246168-run
components:
  schemas: {}
  securitySchemes: {}
servers:
  - url: http://218.78.116.24:10883
    description: 测试环境
security: []

```

# 搜索视频号

## OpenAPI

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /gewe/v2/api/finder/search:
    post:
      summary: 搜索视频号
      deprecated: false
      description: ''
      tags:
        - 基础API/视频号模块
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
                content:
                  type: string
                  description: 搜索内容
                category:
                  type: integer
                  description: '搜索类型，1: 搜索全部 2: 搜索账号（视频号ID）'
                filter:
                  type: integer
                  description: '筛选，0: 不限  1: 最新  2: 朋友赞过'
                page:
                  type: integer
                  description: 首次传0，后续调用时每次加1
                cookie:
                  type: string
                  description: 首次传空，后续传接口返回的data.cookies字段
                searchId:
                  type: string
                  description: 首次传空，后续传接口返回的data.searchID字段
                offset:
                  type: integer
                  description: 首次传0，后续传接口返回的data.offset字段
              required:
                - appId
                - content
              x-apifox-orders:
                - appId
                - content
                - category
                - filter
                - page
                - cookie
                - searchId
                - offset
            example:
              appId: '{{appid}}'
              proxyIp: ''
              content: 人民日报
              category: 1
              filter: 0
              page: 0
              cookie: ''
              searchId: ''
              offset: 0
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
                      advanceSearch:
                        type: object
                        properties:
                          filters:
                            type: array
                            items:
                              type: object
                              properties:
                                column:
                                  type: integer
                                  description: 条件个数
                                display:
                                  type: integer
                                  description: 是否展示
                                options:
                                  type: array
                                  items:
                                    type: object
                                    properties:
                                      paramKey:
                                        type: string
                                        description: 搜索的key
                                      paramValue:
                                        type: string
                                        description: 搜索的value
                                      reportId:
                                        type: string
                                      selected:
                                        type: integer
                                        description: '是否选中，选中:1 '
                                      title:
                                        type: string
                                        description: 搜索描述
                                      type:
                                        type: integer
                                    required:
                                      - paramKey
                                      - paramValue
                                      - reportId
                                      - title
                                      - type
                                    x-apifox-orders:
                                      - paramKey
                                      - paramValue
                                      - reportId
                                      - selected
                                      - title
                                      - type
                                paramKey:
                                  type: string
                                title:
                                  type: string
                                type:
                                  type: integer
                              x-apifox-orders:
                                - column
                                - display
                                - options
                                - paramKey
                                - title
                                - type
                            description: 搜索类型
                          isHold:
                            type: integer
                          showType:
                            type: integer
                        required:
                          - filters
                          - isHold
                          - showType
                        x-apifox-orders:
                          - filters
                          - isHold
                          - showType
                        description: 搜索条件
                      continueFlag:
                        type: integer
                        description: 是否还可以继续翻页，是:1  否:其他
                      cookies:
                        type: string
                        description: 搜索的cookies
                      data:
                        type: array
                        items:
                          type: object
                          properties:
                            boxID:
                              type: string
                            boxPos:
                              type: integer
                            boxPosMerge:
                              type: integer
                            count:
                              type: integer
                            items:
                              type: array
                              items:
                                type: object
                                properties:
                                  desc:
                                    type: string
                                    description: 视频描述
                                  docID:
                                    type: string
                                  jumpInfo:
                                    type: object
                                    properties:
                                      commentScene:
                                        type: integer
                                      jumpType:
                                        type: integer
                                      reportExtraInfo:
                                        type: string
                                      userName:
                                        type: string
                                    required:
                                      - commentScene
                                      - jumpType
                                      - reportExtraInfo
                                      - userName
                                    x-apifox-orders:
                                      - commentScene
                                      - jumpType
                                      - reportExtraInfo
                                      - userName
                                  reportId:
                                    type: string
                                  report_extinfo_str:
                                    type: string
                                  thumbUrl:
                                    type: string
                                    description: 视频封面图
                                  title:
                                    type: string
                                    description: 视频标题
                                x-apifox-orders:
                                  - desc
                                  - docID
                                  - jumpInfo
                                  - reportId
                                  - report_extinfo_str
                                  - thumbUrl
                                  - title
                            moreInfo:
                              type: object
                              properties:
                                moreID:
                                  type: string
                                reportId:
                                  type: string
                              required:
                                - moreID
                                - reportId
                              x-apifox-orders:
                                - moreID
                                - reportId
                            moreText:
                              type: string
                            real_type:
                              type: integer
                            totalCount:
                              type: integer
                            type:
                              type: integer
                            subBoxes:
                              type: array
                              items:
                                type: object
                                properties:
                                  boxID:
                                    type: string
                                  boxMergeType:
                                    type: integer
                                  boxMergeValue:
                                    type: integer
                                  boxPos:
                                    type: integer
                                  boxPosMerge:
                                    type: integer
                                  count:
                                    type: integer
                                  items:
                                    type: array
                                    items:
                                      type: object
                                      properties:
                                        dateTime:
                                          type: string
                                        docID:
                                          type: string
                                        duration:
                                          type: string
                                        image:
                                          type: string
                                        imageData:
                                          type: object
                                          properties:
                                            height:
                                              type: integer
                                            url:
                                              type: string
                                            width:
                                              type: integer
                                          required:
                                            - height
                                            - url
                                            - width
                                          x-apifox-orders:
                                            - height
                                            - url
                                            - width
                                        jumpInfo:
                                          type: object
                                          properties:
                                            extInfo:
                                              type: string
                                            feedId:
                                              type: string
                                            jumpType:
                                              type: integer
                                          required:
                                            - extInfo
                                            - feedId
                                            - jumpType
                                          x-apifox-orders:
                                            - extInfo
                                            - feedId
                                            - jumpType
                                        likeNum:
                                          type: string
                                        noPlayIcon:
                                          type: boolean
                                        pubTime:
                                          type: integer
                                        reportId:
                                          type: string
                                        report_extinfo_str:
                                          type: string
                                        showType:
                                          type: integer
                                        source:
                                          type: object
                                          properties:
                                            iconUrl:
                                              type: string
                                            title:
                                              type: string
                                          required:
                                            - iconUrl
                                            - title
                                          x-apifox-orders:
                                            - iconUrl
                                            - title
                                        title:
                                          type: string
                                        videoUrl:
                                          type: string
                                        report_iteminfo_list_str:
                                          type: string
                                      required:
                                        - dateTime
                                        - docID
                                        - duration
                                        - image
                                        - imageData
                                        - jumpInfo
                                        - likeNum
                                        - noPlayIcon
                                        - pubTime
                                        - reportId
                                        - report_extinfo_str
                                        - showType
                                        - source
                                        - title
                                        - videoUrl
                                        - report_iteminfo_list_str
                                      x-apifox-orders:
                                        - dateTime
                                        - docID
                                        - duration
                                        - image
                                        - imageData
                                        - jumpInfo
                                        - likeNum
                                        - noPlayIcon
                                        - pubTime
                                        - reportId
                                        - report_extinfo_str
                                        - showType
                                        - source
                                        - title
                                        - videoUrl
                                        - report_iteminfo_list_str
                                  moreInfo:
                                    type: object
                                    properties:
                                      moreID:
                                        type: string
                                    required:
                                      - moreID
                                    x-apifox-orders:
                                      - moreID
                                  moreText:
                                    type: string
                                  real_type:
                                    type: integer
                                  resultType:
                                    type: integer
                                  subType:
                                    type: integer
                                  totalCount:
                                    type: integer
                                  type:
                                    type: integer
                                required:
                                  - boxID
                                  - boxMergeValue
                                  - boxPos
                                  - boxPosMerge
                                  - count
                                  - items
                                  - moreInfo
                                  - moreText
                                  - real_type
                                  - resultType
                                  - subType
                                  - totalCount
                                  - type
                                x-apifox-orders:
                                  - boxID
                                  - boxMergeType
                                  - boxMergeValue
                                  - boxPos
                                  - boxPosMerge
                                  - count
                                  - items
                                  - moreInfo
                                  - moreText
                                  - real_type
                                  - resultType
                                  - subType
                                  - totalCount
                                  - type
                          required:
                            - moreInfo
                            - type
                          x-apifox-orders:
                            - boxID
                            - boxPos
                            - boxPosMerge
                            - count
                            - items
                            - moreInfo
                            - moreText
                            - real_type
                            - totalCount
                            - type
                            - subBoxes
                      direction:
                        type: integer
                      experiment:
                        type: array
                        items:
                          type: object
                          properties:
                            key:
                              type: string
                            value:
                              type: string
                          x-apifox-orders:
                            - key
                            - value
                      feedback:
                        type: object
                        properties:
                          isFromMixerMainSwap:
                            type: integer
                        required:
                          - isFromMixerMainSwap
                        x-apifox-orders:
                          - isFromMixerMainSwap
                      isBoxCardStyle:
                        type: integer
                      isDivide:
                        type: integer
                      isHomePage:
                        type: integer
                      lang:
                        type: string
                        description: 语言
                      offset:
                        type: integer
                        description: 偏移量
                      pageNumber:
                        type: integer
                        description: 页码
                      query:
                        type: string
                        description: 搜索的内容
                      resultType:
                        type: integer
                      ret:
                        type: integer
                      searchID:
                        type: string
                        description: 搜索的ID
                      timeStamp:
                        type: integer
                        description: 搜索的时间戳
                    required:
                      - advanceSearch
                      - continueFlag
                      - cookies
                      - data
                      - direction
                      - experiment
                      - feedback
                      - isBoxCardStyle
                      - isDivide
                      - isHomePage
                      - lang
                      - offset
                      - pageNumber
                      - query
                      - resultType
                      - ret
                      - searchID
                      - timeStamp
                    x-apifox-orders:
                      - advanceSearch
                      - continueFlag
                      - cookies
                      - data
                      - direction
                      - experiment
                      - feedback
                      - isBoxCardStyle
                      - isDivide
                      - isHomePage
                      - lang
                      - offset
                      - pageNumber
                      - query
                      - resultType
                      - ret
                      - searchID
                      - timeStamp
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
                  advanceSearch:
                    filters:
                      - column: 3
                        display: 1
                        options:
                          - paramKey: HomePageFinderAdvanceSearchType
                            paramValue: '0'
                            reportId: >-
                              HomePageFinderAdvanceSearchType_0:filter_option:2058117972
                            selected: 1
                            title: 不限
                            type: 1
                          - paramKey: HomePageFinderAdvanceSearchType
                            paramValue: '1'
                            reportId: >-
                              HomePageFinderAdvanceSearchType_1:filter_option:982515211
                            title: 最新
                            type: 1
                          - paramKey: HomePageFinderAdvanceSearchType
                            paramValue: '2'
                            reportId: >-
                              HomePageFinderAdvanceSearchType_2:filter_option:1332662121
                            title: 朋友赞过
                            type: 1
                        paramKey: HomePageFinderAdvanceSearchType
                        title: ''
                        type: 1
                    isHold: 0
                    showType: 5
                  continueFlag: 1
                  cookies: >
                    {"box_offset":0,"businessType":14,"cookies_buffer":"UlYIexABGA4iDOS6uuawkeaXpeaKpTI0MHg4MDAwMDAwMDAwMDAtMC07MHg4MDAwMDAwMC0wLTEwNTk0MTI2MjY0NzY0Njk3Mjk4O1ABeAmCAQUQAKIBAA==","doc_offset":0,"dup_bf":"0x800000000000-0-;0x80000000-0-10594126264764697298;","isHomepage":0,"page_cnt":1,"query":"人民日报","scene":123}
                  data:
                    - boxID: 0x800000000000-0-
                      boxPos: 1
                      boxPosMerge: 1
                      count: 1
                      items:
                        - desc: 参与、沟通、记录时代。
                          docID: >-
                            finderacctv04NKr31L/vjdDvpFKTbggRtW22xzBBv0xfGlfNYMc23k=
                          jumpInfo:
                            commentScene: 6
                            jumpType: 7
                            reportExtraInfo: |
                              {}
                            userName: >-
                              v2_060000231003b20faec8c6e4811dc1d4c602ee30b0771bbcf220c67926bb76ab7702ac335a53@finder
                          reportId: >-
                            finderacctv04NKr31L/vjdDvpFKTbggRiYnkYx1UxCkmG5moUVOxbWxCefvE3aNSdPQXM62q1/f
                          report_extinfo_str: ''
                          thumbUrl: >-
                            https://wx.qlogo.cn/finderhead/ver_1/hmT61UloVtTOIVa3JC9KYzgHClDdlWW36QrL3ib0yjtxA4utJjGWWG1JQibnCEYYicCCHPh8hxX9hcxv4lZR4QWxQ/132
                          title: <em class="highlight">人民日报</em>
                      moreInfo:
                        moreID: '33554434'
                        reportId: more:more:972956
                      moreText: 更多
                      real_type: 33554434
                      totalCount: 136
                      type: 62
                    - moreInfo:
                        moreID: ''
                        reportId: ''
                      type: 110
                      subBoxes:
                        - boxID: 0x80000000000-1-14311466688778406235
                          boxMergeType: 110
                          boxMergeValue: 4
                          boxPos: 2
                          boxPosMerge: 2
                          count: 1
                          items:
                            - dateTime: 6小时前
                              docID: '14311466688778406235'
                              duration: '00:21'
                              image: >-
                                http://wxapp.tc.qq.com/251/20304/stodownload?encfilekey=rjD5jyTuFrIpZ2ibE8T7YmwgiahniaXswqz4NuaSKsFibGUlfJ5hU4ZDW9ciarOqPHtHibYGRTzzw81mVAhh7DFC9YK7zWPjQnYe9ZH31OW8icQyq4Svxm0ibHBgAQ&bizid=1023&dotrans=0&hy=SH&idx=1&m=&scene=0&token=cztXnd9GyrFic3jndkicLXIMb0jg4HJuaLaOKSgp63dThnqIib6xric0XbAEKE7T6cAv
                              imageData:
                                height: 1920
                                url: >-
                                  http://wxapp.tc.qq.com/251/20304/stodownload?encfilekey=rjD5jyTuFrIpZ2ibE8T7YmwgiahniaXswqz4NuaSKsFibGUlfJ5hU4ZDW9ciarOqPHtHibYGRTzzw81mVAhh7DFC9YK7zWPjQnYe9ZH31OW8icQyq4Svxm0ibHBgAQ&bizid=1023&dotrans=0&hy=SH&idx=1&m=&scene=0&token=cztXnd9GyrFic3jndkicLXIMb0jg4HJuaLaOKSgp63dThnqIib6xric0XbAEKE7T6cAv
                                width: 1080
                              jumpInfo:
                                extInfo: >
                                  {"behavior":["report_feed_read","allow_pull_top","allow_infinite_top_pull"],"encryptedObjectId":"export/UzFfAgtgekIEAQAAAAAAEEUq50vvzgAAAAstQy6ubaLX4KHWvLEZgBPEj6EUBRwIeKuFzNPgMIqnjM-K11J3xUUainxgt8i0","feedFocusChangeNotify":true,"feedNonceId":"9851034887115316022","getRelatedList":true,"reportExtraInfo":"{\"report_json\":\"\"}\n","reportScene":14,"requestScene":13,"sessionId":"CNuS5LuM5KLOxgEI6ZKcubXMrs3GAQjIksjH_JG5zMYBCOGSgMv078HOxgEIwLGA-N-Gls7GAQjEkITrl-uNy8YBCN2SzJWcxNCexgEIjpDoptyzxLvEAQjJktiB8p6SrMYBCO6S7MbP9qSmxgEI6pHMlaeyt9rEARC5l8DinZCDkOABKgzkurrmsJHml6XmiqUwADiAgICAgIACQAFQtZeZmA8."}
                                feedId: '14311466688778406235'
                                jumpType: 9
                              likeNum: 8.9万
                              noPlayIcon: true
                              pubTime: 1706059776
                              reportId: 14311466688778406235:feed:0
                              report_extinfo_str: >-
                                %7B%22friend_like%22%3A0%2C%22item_tab%22%3A14%2C%22session_buffer%22%3A%22%7B%5C%22object_id%5C%22%3A14311466688778406235%2C%5C%22request_id%5C%22%3A16149922015637146553%2C%5C%22media_type%5C%22%3A0%2C%5C%22vid_len%5C%22%3A21%2C%5C%22create_time%5C%22%3A1706059776%2C%5C%22delivery_time%5C%22%3A1706083020%2C%5C%22comment_scene%5C%22%3A180%2C%5C%22delivery_scene%5C%22%3A76%2C%5C%22set_condition_flag%5C%22%3A51%2C%5C%22device_type_id%5C%22%3A13%2C%5C%22feed_pos%5C%22%3A0%7D%22%2C%22duration%22%3A21%2C%22upload_time%22%3A1706059776%7D
                              showType: 1
                              source:
                                iconUrl: >-
                                  https://wx.qlogo.cn/finderhead/ver_1/Eqf9VR6ArnSSAcFpMlIUW5AuTBpg2CZMPntNoeW5Un4RRVtD9EliboOT0VTJ7jqE9LzUvqwNRSeSwmbluyacxYw/132
                                title: <em class="highlight">人民日报</em>
                              title: “我正在抢救病人，地震我也不能走。”地震瞬间，他们选择为患者继续完成手术。致敬医者仁心！
                              videoUrl: >-
                                https://findermp.video.qq.com/251/20302/stodownload?encfilekey=Cvvj5Ix3eewK0tHtibORqcsqchXNh0Gf3sJcaYqC2rQA3ywV5oEa4CeTyCbKESan8ZsCsReiadrpqJmJ8n6e4RjfrycdJTpTfXvHVriaIvC4T6ic6icVMMEP3XqLbia0YDs02ib&bizid=1023&dotrans=0&hy=SH&idx=1&m=&upid=0&partscene=4&X-snsvideoflag=xWT111&token=AxricY7RBHdVnQlzgG2jDJnXVhI55NowAOcf0udBhNN7OmdL2ibqb4d5AFEqFicsKaVej8ygjq0cvE
                          moreInfo:
                            moreID: '4313841664'
                          moreText: 更多
                          real_type: 18874368
                          resultType: 0
                          subType: 1
                          totalCount: 293
                          type: 86
                        - boxID: 0x80000000000-1-14310955701749877097
                          boxMergeValue: 4
                          boxPos: 3
                          boxPosMerge: 2
                          count: 1
                          items:
                            - dateTime: 23小时前
                              docID: '14310955701749877097'
                              duration: '00:17'
                              image: >-
                                http://wxapp.tc.qq.com/251/20304/stodownload?encfilekey=rjD5jyTuFrIpZ2ibE8T7Ym3K77SEULgkiadmluVrMOeKmyN9Iq2OiaIVUkrBCZ5Hr95cIyec8fOj43iaQVibF2GSvl9oLQGDtqQJ7NZLeI1nge2vy28ARzmoYew&bizid=1023&dotrans=0&hy=SZ&idx=1&m=&scene=0&token=x5Y29zUxcibDHxWfF8R3ao53AuSNDZibrFkyR7ErAcZwLH8DteMDAdF9pegzyX3nC6
                              imageData:
                                height: 1440
                                url: >-
                                  http://wxapp.tc.qq.com/251/20304/stodownload?encfilekey=rjD5jyTuFrIpZ2ibE8T7Ym3K77SEULgkiadmluVrMOeKmyN9Iq2OiaIVUkrBCZ5Hr95cIyec8fOj43iaQVibF2GSvl9oLQGDtqQJ7NZLeI1nge2vy28ARzmoYew&bizid=1023&dotrans=0&hy=SZ&idx=1&m=&scene=0&token=x5Y29zUxcibDHxWfF8R3ao53AuSNDZibrFkyR7ErAcZwLH8DteMDAdF9pegzyX3nC6
                                width: 1080
                              jumpInfo:
                                extInfo: >
                                  {"behavior":["report_feed_read","allow_pull_top","allow_infinite_top_pull"],"encryptedObjectId":"export/UzFfAgtgekIEAQAAAAAAWcYyy4gU3gAAAAstQy6ubaLX4KHWvLEZgBPEvaFsByUgdKiFzNPgMIqvj6M34S3A7WjVyhC5EJgU","feedFocusChangeNotify":true,"feedNonceId":"4311808773913630305","getRelatedList":true,"reportExtraInfo":"{\"report_json\":\"\"}\n","reportScene":14,"requestScene":13,"sessionId":"CNuS5LuM5KLOxgEI6ZKcubXMrs3GAQjIksjH_JG5zMYBCOGSgMv078HOxgEIwLGA-N-Gls7GAQjEkITrl-uNy8YBCN2SzJWcxNCexgEIjpDoptyzxLvEAQjJktiB8p6SrMYBCO6S7MbP9qSmxgEI6pHMlaeyt9rEARC5l8DinZCDkOABKgzkurrmsJHml6XmiqUwADiAgICAgIACQAFQtZeZmA8."}
                                feedId: '14310955701749877097'
                                jumpType: 9
                              likeNum: 3.4万
                              noPlayIcon: true
                              pubTime: 1705998862
                              reportId: 14310955701749877097:feed:0
                              report_extinfo_str: >-
                                %7B%22friend_like%22%3A0%2C%22item_tab%22%3A14%2C%22session_buffer%22%3A%22%7B%5C%22object_id%5C%22%3A14310955701749877097%2C%5C%22request_id%5C%22%3A16149922015637146553%2C%5C%22media_type%5C%22%3A0%2C%5C%22vid_len%5C%22%3A17%2C%5C%22create_time%5C%22%3A1705998862%2C%5C%22delivery_time%5C%22%3A1706083020%2C%5C%22comment_scene%5C%22%3A180%2C%5C%22delivery_scene%5C%22%3A76%2C%5C%22set_condition_flag%5C%22%3A51%2C%5C%22device_type_id%5C%22%3A13%2C%5C%22feed_pos%5C%22%3A0%7D%22%2C%22duration%22%3A17%2C%22upload_time%22%3A1705998862%7D
                              showType: 1
                              source:
                                iconUrl: >-
                                  https://wx.qlogo.cn/finderhead/ver_1/Eqf9VR6ArnSSAcFpMlIUW5AuTBpg2CZMPntNoeW5Un4RRVtD9EliboOT0VTJ7jqE9LzUvqwNRSeSwmbluyacxYw/132
                                title: <em class="highlight">人民日报</em>
                              title: 地震发生时，她的第一反应不是逃生，而是奔跑着疏散旅客。致敬坚守！
                              videoUrl: >-
                                https://findermp.video.qq.com/251/20302/stodownload?encfilekey=Cvvj5Ix3eewK0tHtibORqcsqchXNh0Gf3sJcaYqC2rQCGYI2ibbL64KybEQbzicuf2y3VkcHibsqiangYqSIibWFtyJcEpia24WSES1bYfBuTRHGLRcRIFR0fJDkzPuY7EmNdxB&bizid=1023&dotrans=0&hy=SH&idx=1&m=&upid=0&partscene=4&X-snsvideoflag=xWT111&token=x5Y29zUxcibAicmfnZH1zhR57wRxr0Oq4EyRFHTgKcNSEm6z28boIOVD22CeOgN5Hqp7PTCPVsKbI
                              report_iteminfo_list_str: 14310955701749877097:feed:0
                          moreInfo:
                            moreID: '4313841664'
                          moreText: 更多
                          real_type: 18874368
                          resultType: 0
                          subType: 1
                          totalCount: 293
                          type: 86
                        - boxID: 0x80000000000-1-14310439122172512584
                          boxMergeValue: 4
                          boxPos: 4
                          boxPosMerge: 2
                          count: 1
                          items:
                            - dateTime: 1天前
                              docID: '14310439122172512584'
                              duration: '01:11'
                              image: >-
                                http://wxapp.tc.qq.com/251/20304/stodownload?encfilekey=rjD5jyTuFrIpZ2ibE8T7YmwgiahniaXswqzh8Y7mSrUU7PsF7jeWsWVkVjMOJXialHuCtVj1uwpaYqSibadpn8kYxG1iauADC2tiaaTV3rrcs08Y5pKpKtzvgkJjA&bizid=1023&dotrans=0&hy=SH&idx=1&m=&scene=0&token=cztXnd9GyrH5K7HJTl5SevaiaEntakf1R8OwUNCtaBYVzRkenXFppBTTY5MzggK6d
                              imageData:
                                height: 1440
                                url: >-
                                  http://wxapp.tc.qq.com/251/20304/stodownload?encfilekey=rjD5jyTuFrIpZ2ibE8T7YmwgiahniaXswqzh8Y7mSrUU7PsF7jeWsWVkVjMOJXialHuCtVj1uwpaYqSibadpn8kYxG1iauADC2tiaaTV3rrcs08Y5pKpKtzvgkJjA&bizid=1023&dotrans=0&hy=SH&idx=1&m=&scene=0&token=cztXnd9GyrH5K7HJTl5SevaiaEntakf1R8OwUNCtaBYVzRkenXFppBTTY5MzggK6d
                                width: 1080
                              jumpInfo:
                                extInfo: >
                                  {"behavior":["report_feed_read","allow_pull_top","allow_infinite_top_pull"],"encryptedObjectId":"export/UzFfAgtgekIEAQAAAAAAXV8Yqa-2FQAAAAstQy6ubaLX4KHWvLEZgBPEnKE4eWx9Y6mFzNPgMIpacfdfY7SlrFC-C0niIBlM","feedFocusChangeNotify":true,"feedNonceId":"13355705465228783016","getRelatedList":true,"reportExtraInfo":"{\"report_json\":\"\"}\n","reportScene":14,"requestScene":13,"sessionId":"CNuS5LuM5KLOxgEI6ZKcubXMrs3GAQjIksjH_JG5zMYBCOGSgMv078HOxgEIwLGA-N-Gls7GAQjEkITrl-uNy8YBCN2SzJWcxNCexgEIjpDoptyzxLvEAQjJktiB8p6SrMYBCO6S7MbP9qSmxgEI6pHMlaeyt9rEARC5l8DinZCDkOABKgzkurrmsJHml6XmiqUwADiAgICAgIACQAFQtZeZmA8."}
                                feedId: '14310439122172512584'
                                jumpType: 9
                              likeNum: 1万
                              noPlayIcon: true
                              pubTime: 1705937280
                              reportId: 14310439122172512584:feed:0
                              report_extinfo_str: >-
                                %7B%22friend_like%22%3A0%2C%22item_tab%22%3A14%2C%22session_buffer%22%3A%22%7B%5C%22object_id%5C%22%3A14310439122172512584%2C%5C%22request_id%5C%22%3A16149922015637146553%2C%5C%22media_type%5C%22%3A0%2C%5C%22vid_len%5C%22%3A71%2C%5C%22create_time%5C%22%3A1705937280%2C%5C%22delivery_time%5C%22%3A1706083020%2C%5C%22comment_scene%5C%22%3A180%2C%5C%22delivery_scene%5C%22%3A76%2C%5C%22set_condition_flag%5C%22%3A51%2C%5C%22device_type_id%5C%22%3A13%2C%5C%22feed_pos%5C%22%3A0%7D%22%2C%22duration%22%3A71%2C%22upload_time%22%3A1705937280%7D
                              showType: 1
                              source:
                                iconUrl: >-
                                  https://wx.qlogo.cn/finderhead/ver_1/Eqf9VR6ArnSSAcFpMlIUW5AuTBpg2CZMPntNoeW5Un4RRVtD9EliboOT0VTJ7jqE9LzUvqwNRSeSwmbluyacxYw/132
                                title: <em class="highlight">人民日报</em>
                              title: >-
                                ...要看<em
                                class="highlight">人民</em>群众满意不满意。这份情怀，始终如一。
                              videoUrl: >-
                                https://findermp.video.qq.com/251/20302/stodownload?encfilekey=Cvvj5Ix3eewK0tHtibORqcsqchXNh0Gf3sJcaYqC2rQAlONzzCSMuKScUSqk6UmlJUNPCOcPibELibDh0aTYWibfopJFlnzWIHEoeQgKbCuUOfj5HJz56xQF939icxpJfQMjE&bizid=1023&dotrans=0&hy=SH&idx=1&m=&upid=0&partscene=4&X-snsvideoflag=xWT111&token=AxricY7RBHdVnQlzgG2jDJjGcmyLrD6KppkTvCtoc6GEqhOGbbibDNwiaer5DzroU4atjruD2H5wrI
                              report_iteminfo_list_str: 14310439122172512584:feed:0
                          moreInfo:
                            moreID: '4313841664'
                          moreText: 更多
                          real_type: 18874368
                          resultType: 0
                          subType: 1
                          totalCount: 293
                          type: 86
                        - boxID: 0x80000000000-1-14311603434126575969
                          boxMergeValue: 4
                          boxPos: 5
                          boxPosMerge: 2
                          count: 1
                          items:
                            - dateTime: 1小时前
                              docID: '14311603434126575969'
                              duration: '00:15'
                              image: >-
                                http://wxapp.tc.qq.com/251/20304/stodownload?encfilekey=rjD5jyTuFrIpZ2ibE8T7YmwgiahniaXswqzaMKW0oib0Dvo8dxu4mqTgGibRSiarVQ22a4ibnNw6318YpXf7lyZY7nJaIeTHOJ5a7Zyg1vibb5tCWMdh157GMibq9UA&bizid=1023&dotrans=0&hy=SH&idx=1&m=&scene=0&token=x5Y29zUxcibDL4kjgECWmgfJh1nfZicMEFhgaJNxiaEibCTr1xtyKiajq9O6LDDQ1YjX9
                              imageData:
                                height: 1920
                                url: >-
                                  http://wxapp.tc.qq.com/251/20304/stodownload?encfilekey=rjD5jyTuFrIpZ2ibE8T7YmwgiahniaXswqzaMKW0oib0Dvo8dxu4mqTgGibRSiarVQ22a4ibnNw6318YpXf7lyZY7nJaIeTHOJ5a7Zyg1vibb5tCWMdh157GMibq9UA&bizid=1023&dotrans=0&hy=SH&idx=1&m=&scene=0&token=x5Y29zUxcibDL4kjgECWmgfJh1nfZicMEFhgaJNxiaEibCTr1xtyKiajq9O6LDDQ1YjX9
                                width: 1080
                              jumpInfo:
                                extInfo: >
                                  {"behavior":["report_feed_read","allow_pull_top","allow_infinite_top_pull"],"encryptedObjectId":"export/UzFfAgtgekIEAQAAAAAA-S4u-54M3wAAAAstQy6ubaLX4KHWvLEZgBPEtaFwdWQDG6uFzNPgMIrZfpaZyRrY-SJpM2APGQe7","feedFocusChangeNotify":true,"feedNonceId":"3842447460607405520","getRelatedList":true,"reportExtraInfo":"{\"report_json\":\"\"}\n","reportScene":14,"requestScene":13,"sessionId":"CNuS5LuM5KLOxgEI6ZKcubXMrs3GAQjIksjH_JG5zMYBCOGSgMv078HOxgEIwLGA-N-Gls7GAQjEkITrl-uNy8YBCN2SzJWcxNCexgEIjpDoptyzxLvEAQjJktiB8p6SrMYBCO6S7MbP9qSmxgEI6pHMlaeyt9rEARC5l8DinZCDkOABKgzkurrmsJHml6XmiqUwADiAgICAgIACQAFQtZeZmA8."}
                                feedId: '14311603434126575969'
                                jumpType: 9
                              likeNum: '492'
                              noPlayIcon: true
                              pubTime: 1706076077
                              reportId: 14311603434126575969:feed:0
                              report_extinfo_str: >-
                                %7B%22friend_like%22%3A0%2C%22item_tab%22%3A14%2C%22session_buffer%22%3A%22%7B%5C%22object_id%5C%22%3A14311603434126575969%2C%5C%22request_id%5C%22%3A16149922015637146553%2C%5C%22media_type%5C%22%3A0%2C%5C%22vid_len%5C%22%3A15%2C%5C%22create_time%5C%22%3A1706076077%2C%5C%22delivery_time%5C%22%3A1706083020%2C%5C%22comment_scene%5C%22%3A180%2C%5C%22delivery_scene%5C%22%3A76%2C%5C%22set_condition_flag%5C%22%3A51%2C%5C%22device_type_id%5C%22%3A13%2C%5C%22feed_pos%5C%22%3A0%7D%22%2C%22duration%22%3A15%2C%22upload_time%22%3A1706076077%7D
                              showType: 1
                              source:
                                iconUrl: >-
                                  https://wx.qlogo.cn/finderhead/ver_1/Eqf9VR6ArnSSAcFpMlIUW5AuTBpg2CZMPntNoeW5Un4RRVtD9EliboOT0VTJ7jqE9LzUvqwNRSeSwmbluyacxYw/132
                                title: <em class="highlight">人民日报</em>
                              title: 现场视频！中国和瑙鲁恢复外交关系。
                              videoUrl: >-
                                https://findermp.video.qq.com/251/20302/stodownload?encfilekey=Cvvj5Ix3eewK0tHtibORqcsqchXNh0Gf3sJcaYqC2rQBksia3pqnkQria8yvLBl9XZoBwLHmymaqPlWSaeYpE3Fj2hbQGE3E3bruMp5B9M218PUG0SL55Zc2XFucMV9JAaD&bizid=1023&dotrans=0&hy=SH&idx=1&m=&upid=0&partscene=4&X-snsvideoflag=xWT111&token=x5Y29zUxcibAicmfnZH1zhRw0Yyn8WKP5Y4uSNg3tiajibr27mMHfucnPibNMhu6jSGF45XjVnQayDibk
                              report_iteminfo_list_str: 14311603434126575969:feed:0
                          moreInfo:
                            moreID: '4313841664'
                          moreText: 更多
                          real_type: 18874368
                          resultType: 0
                          subType: 1
                          totalCount: 293
                          type: 86
                        - boxID: 0x80000000-0-10594126264764697298
                          boxMergeValue: 4
                          boxPos: 6
                          boxPosMerge: 2
                          count: 1
                          items:
                            - dateTime: ''
                              docID: '10594126264764697298'
                              duration: ''
                              image: ''
                              imageData:
                                height: 0
                                url: ''
                                width: 0
                              jumpInfo:
                                extInfo: ''
                                feedId: ''
                                jumpType: 2
                              noPlayIcon: false
                              pubTime: 0
                              reportId: ''
                              report_extinfo_str: ''
                              showType: 3
                              source:
                                iconUrl: >-
                                  http://mmbiz.qpic.cn/wx_search/7OFQAWlVg1rQsruqlr2vKQzjdcIcBPz5cJ3EkkMicI68/0
                                title: 搜狗百科小程序
                              title: <em class="highlight">人民日报</em> - 百科
                              videoUrl: ''
                              report_iteminfo_list_str: panel:panel:734903
                          moreInfo:
                            moreID: ''
                          moreText: ''
                          real_type: 16777728
                          resultType: 1
                          subType: 0
                          totalCount: 1
                          type: 16777728
                        - boxID: 0x80000000000-1-14311410704811301056
                          boxMergeValue: 4
                          boxPos: 7
                          boxPosMerge: 2
                          count: 1
                          items:
                            - dateTime: 8小时前
                              docID: '14311410704811301056'
                              duration: '00:44'
                              image: >-
                                http://wxapp.tc.qq.com/251/20304/stodownload?encfilekey=oibeqyX228riaCwo9STVsGLPj9UYCicgttvClHWTGFqpRicN4VPS7Ug5rVbQPibvibaa9cQsWHppp5iccQp1YribNxJKP3XbufEdyKtVhqZubRM5emcAV0tcwVBRJnL9WzuGpn3WPFceCm5xNic8&bizid=1023&dotrans=0&hy=SH&idx=1&m=dede79704d39a48edbf9fda313b9adb6&token=x5Y29zUxcibB5swgCmOQ85u2j6T8sGzvTs32XxibKTct5odj3Lw025JCltgZeUq62ia
                              imageData:
                                height: 1280
                                url: >-
                                  http://wxapp.tc.qq.com/251/20304/stodownload?encfilekey=oibeqyX228riaCwo9STVsGLPj9UYCicgttvClHWTGFqpRicN4VPS7Ug5rVbQPibvibaa9cQsWHppp5iccQp1YribNxJKP3XbufEdyKtVhqZubRM5emcAV0tcwVBRJnL9WzuGpn3WPFceCm5xNic8&bizid=1023&dotrans=0&hy=SH&idx=1&m=dede79704d39a48edbf9fda313b9adb6&token=x5Y29zUxcibB5swgCmOQ85u2j6T8sGzvTs32XxibKTct5odj3Lw025JCltgZeUq62ia
                                width: 720
                              jumpInfo:
                                extInfo: >
                                  {"behavior":["report_feed_read","allow_pull_top","allow_infinite_top_pull"],"encryptedObjectId":"export/UzFfAgtgekIEAQAAAAAARRQaI1CXnAAAAAstQy6ubaLX4KHWvLEZgBPElIJwRk9qTKuFzNPgMIqIfaV3vYI2gp93aAyUjUxs","feedFocusChangeNotify":true,"feedNonceId":"16013487545239562461","getRelatedList":true,"reportExtraInfo":"{\"report_json\":\"\"}\n","reportScene":14,"requestScene":13,"sessionId":"CNuS5LuM5KLOxgEI6ZKcubXMrs3GAQjIksjH_JG5zMYBCOGSgMv078HOxgEIwLGA-N-Gls7GAQjEkITrl-uNy8YBCN2SzJWcxNCexgEIjpDoptyzxLvEAQjJktiB8p6SrMYBCO6S7MbP9qSmxgEI6pHMlaeyt9rEARC5l8DinZCDkOABKgzkurrmsJHml6XmiqUwADiAgICAgIACQAFQtZeZmA8."}
                                feedId: '14311410704811301056'
                                jumpType: 9
                              likeNum: '18'
                              noPlayIcon: true
                              pubTime: 1706053102
                              reportId: 14311410704811301056:feed:0
                              report_extinfo_str: >-
                                %7B%22friend_like%22%3A0%2C%22item_tab%22%3A14%2C%22session_buffer%22%3A%22%7B%5C%22object_id%5C%22%3A14311410704811301056%2C%5C%22request_id%5C%22%3A16149922015637146553%2C%5C%22media_type%5C%22%3A0%2C%5C%22vid_len%5C%22%3A44%2C%5C%22create_time%5C%22%3A1706053102%2C%5C%22delivery_time%5C%22%3A1706083020%2C%5C%22comment_scene%5C%22%3A180%2C%5C%22delivery_scene%5C%22%3A76%2C%5C%22set_condition_flag%5C%22%3A51%2C%5C%22device_type_id%5C%22%3A13%2C%5C%22feed_pos%5C%22%3A0%7D%22%2C%22duration%22%3A44%2C%22upload_time%22%3A1706053102%7D
                              showType: 1
                              source:
                                iconUrl: >-
                                  http://wx.qlogo.cn/mmhead/Q3auHgzwzM6amxFj13X4SHHsKtMDI4tYoibsLovsJUmTw5gT8sLUicpQ/132
                                title: I长治
                              title: “中国铁路见证了我们十年的爱情长跑！”“#最贵婚车” 的主人公回应啦。
                              videoUrl: >-
                                https://findermp.video.qq.com/251/20302/stodownload?encfilekey=Cvvj5Ix3eez3Y79SxtvVL0L7CkPM6dFibFeI6caGYwFG4ia5hfIjWRiaiarsgJ77QQDKN5yB839Lg7hqGokJq3I4t3nkQscKQxQbTqp9c9C7m7Em6uUw8aukIopraR1DQDLXN4nokd5GjA4czjAy12UM6Q&bizid=1023&dotrans=0&hy=SH&idx=1&m=8e0b4cc47abd0b6d11dc47dc96e9072b&upid=500270&partscene=4&X-snsvideoflag=xWT111&token=AxricY7RBHdVnQlzgG2jDJiaJdRh1HpichuPxtdDyOMnOmZsXFWaNI5a07WpJ8mHEPZ8WuBqJ7bYCU
                              report_iteminfo_list_str: 14311410704811301056:feed:0
                          moreInfo:
                            moreID: '4313841664'
                          moreText: 更多
                          real_type: 18874368
                          resultType: 0
                          subType: 1
                          totalCount: 293
                          type: 86
                        - boxID: 0x80000000000-1-14309685723511457860
                          boxMergeValue: 4
                          boxPos: 8
                          boxPosMerge: 2
                          count: 1
                          items:
                            - dateTime: 2天前
                              docID: '14309685723511457860'
                              duration: '00:56'
                              image: >-
                                http://wxapp.tc.qq.com/251/20304/stodownload?encfilekey=oibeqyX228riaCwo9STVsGLPj9UYCicgttv9qCtC7NHBsK3gSibJNpkcw2d3vvCQzJacyUaPibWcjkMs5ZPKZvkdicN0fU6RQzYrDA0TOj4SEc9t60yA8RnlxlJwZVpPcZicgP9k9AsaBwJFiaE&bizid=1023&dotrans=0&hy=SH&idx=1&m=21cd4c4175c453e73b127981a3b626c2&token=cztXnd9GyrGqKjnmm8EjsKFAlLXKn2KwoliavbnRvHK0uqT9S6X2hhEQQ90cQicskN
                              imageData:
                                height: 1920
                                url: >-
                                  http://wxapp.tc.qq.com/251/20304/stodownload?encfilekey=oibeqyX228riaCwo9STVsGLPj9UYCicgttv9qCtC7NHBsK3gSibJNpkcw2d3vvCQzJacyUaPibWcjkMs5ZPKZvkdicN0fU6RQzYrDA0TOj4SEc9t60yA8RnlxlJwZVpPcZicgP9k9AsaBwJFiaE&bizid=1023&dotrans=0&hy=SH&idx=1&m=21cd4c4175c453e73b127981a3b626c2&token=cztXnd9GyrGqKjnmm8EjsKFAlLXKn2KwoliavbnRvHK0uqT9S6X2hhEQQ90cQicskN
                                width: 1080
                              jumpInfo:
                                extInfo: >
                                  {"behavior":["report_feed_read","allow_pull_top","allow_infinite_top_pull"],"encryptedObjectId":"export/UzFfAgtgekIEAQAAAAAA-3A6y2SprgAAAAstQy6ubaLX4KHWvLEZgBPEkKN0VQcHV66FzNPgMIo1gPvHZdmmWbciZzOb6B6B","feedFocusChangeNotify":true,"feedNonceId":"16498845498073970400","getRelatedList":true,"reportExtraInfo":"{\"report_json\":\"\"}\n","reportScene":14,"requestScene":13,"sessionId":"CNuS5LuM5KLOxgEI6ZKcubXMrs3GAQjIksjH_JG5zMYBCOGSgMv078HOxgEIwLGA-N-Gls7GAQjEkITrl-uNy8YBCN2SzJWcxNCexgEIjpDoptyzxLvEAQjJktiB8p6SrMYBCO6S7MbP9qSmxgEI6pHMlaeyt9rEARC5l8DinZCDkOABKgzkurrmsJHml6XmiqUwADiAgICAgIACQAFQtZeZmA8."}
                                feedId: '14309685723511457860'
                                jumpType: 9
                              likeNum: 1.7万
                              noPlayIcon: true
                              pubTime: 1705847468
                              reportId: 14309685723511457860:feed:0
                              report_extinfo_str: >-
                                %7B%22friend_like%22%3A0%2C%22item_tab%22%3A14%2C%22session_buffer%22%3A%22%7B%5C%22object_id%5C%22%3A14309685723511457860%2C%5C%22request_id%5C%22%3A16149922015637146553%2C%5C%22media_type%5C%22%3A0%2C%5C%22vid_len%5C%22%3A56%2C%5C%22create_time%5C%22%3A1705847468%2C%5C%22delivery_time%5C%22%3A1706083020%2C%5C%22comment_scene%5C%22%3A180%2C%5C%22delivery_scene%5C%22%3A76%2C%5C%22set_condition_flag%5C%22%3A51%2C%5C%22device_type_id%5C%22%3A13%2C%5C%22feed_pos%5C%22%3A0%7D%22%2C%22duration%22%3A56%2C%22upload_time%22%3A1705847468%7D
                              showType: 1
                              source:
                                iconUrl: >-
                                  http://wx.qlogo.cn/mmhead/Q3auHgzwzM4SpgWg8Okg84iaPibMsk7tyVIUQEZfwGZIogiasI0af71ag/132
                                title: 陕西新闻广播
                              title: 事发江西街头！交警执法被<em class="highlight">人民日报</em>“点名”…
                              videoUrl: >-
                                https://findermp.video.qq.com/251/20302/stodownload?encfilekey=Cvvj5Ix3eez3Y79SxtvVL0L7CkPM6dFibFeI6caGYwFH4cxu16ib2NiaCDDv3YDMxLMLicktouLqOXws4qs19JsWicBmKYLib2PrdrkmKxEyGdpj7APGPDyaKpJ2ZVos60R6h8oBxYcJss20icEyygF6pglpg&bizid=1023&dotrans=0&hy=SH&idx=1&m=b575cbbce658b975c4d898de06d0c20b&upid=500090&partscene=4&X-snsvideoflag=xWT111&token=AxricY7RBHdVnQlzgG2jDJiaJdRh1HpichuokXduHlibszrAnwwtGXS28TyeebtiaFEhXu08JuO1U0Ow
                              report_iteminfo_list_str: 14309685723511457860:feed:0
                          moreInfo:
                            moreID: '4313841664'
                          moreText: 更多
                          real_type: 18874368
                          resultType: 0
                          subType: 1
                          totalCount: 293
                          type: 86
                        - boxID: 0x80000000000-1-14284646305856948573
                          boxMergeValue: 4
                          boxPos: 9
                          boxPosMerge: 2
                          count: 1
                          items:
                            - dateTime: 1个月前
                              docID: '14284646305856948573'
                              duration: '01:08'
                              image: >-
                                http://wxapp.tc.qq.com/251/20304/stodownload?encfilekey=rjD5jyTuFrIpZ2ibE8T7YmwgiahniaXswqzfb5ESsHEYDA7AHh4sSccLg0dCLibtWY2iaJv8hic4QpotfrTcAwPyKyh1t4thvjjsfB6K5MID2LpicBg9vLiaxCqwqA&bizid=1023&dotrans=0&hy=SH&idx=1&m=&scene=0&token=cztXnd9GyrFHsCMU8q7YEA4tPEfzzHMfuAgsHH5FeSUXygHY8F1jdhrHicvPicRibNv
                              imageData:
                                height: 1440
                                url: >-
                                  http://wxapp.tc.qq.com/251/20304/stodownload?encfilekey=rjD5jyTuFrIpZ2ibE8T7YmwgiahniaXswqzfb5ESsHEYDA7AHh4sSccLg0dCLibtWY2iaJv8hic4QpotfrTcAwPyKyh1t4thvjjsfB6K5MID2LpicBg9vLiaxCqwqA&bizid=1023&dotrans=0&hy=SH&idx=1&m=&scene=0&token=cztXnd9GyrFHsCMU8q7YEA4tPEfzzHMfuAgsHH5FeSUXygHY8F1jdhrHicvPicRibNv
                                width: 1080
                              jumpInfo:
                                extInfo: >
                                  {"behavior":["report_feed_read","allow_pull_top","allow_infinite_top_pull"],"encryptedObjectId":"export/UzFfAgtgekIEAQAAAAAAm4stvf42ewAAAAstQy6ubaLX4KHWvLEZgBPEiaE8KwwoCvuFzNPgMIo26veYgLZ3YqsETshFS0sq","feedFocusChangeNotify":true,"feedNonceId":"12403360781482303400","getRelatedList":true,"reportExtraInfo":"{\"report_json\":\"\"}\n","reportScene":14,"requestScene":13,"sessionId":"COmSnLm1zK7NxgEIyJLIx_yRuczGAQjhkoDL9O_BzsYBCMCxgPjfhpbOxgEIxJCE65frjcvGAQjdksyVnMTQnsYBCI6Q6Kbcs8S7xAEIyZLYgfKekqzGAQjukuzGz_akpsYBCOqRzJWnsrfaxAEIzpDMzOT8iaPEARC5l8DinZCDkOABKgzkurrmsJHml6XmiqUwADiAgICAgIACQAFQtZeZmA8."}
                                feedId: '14284646305856948573'
                                jumpType: 9
                              likeNum: '6363'
                              noPlayIcon: true
                              pubTime: 1702862537
                              reportId: 14284646305856948573:feed:0
                              report_extinfo_str: >-
                                %7B%22friend_like%22%3A0%2C%22item_tab%22%3A14%2C%22session_buffer%22%3A%22%7B%5C%22object_id%5C%22%3A14284646305856948573%2C%5C%22request_id%5C%22%3A16149922015637146553%2C%5C%22media_type%5C%22%3A0%2C%5C%22vid_len%5C%22%3A68%2C%5C%22create_time%5C%22%3A1702862537%2C%5C%22delivery_time%5C%22%3A1706083020%2C%5C%22comment_scene%5C%22%3A180%2C%5C%22delivery_scene%5C%22%3A76%2C%5C%22set_condition_flag%5C%22%3A51%2C%5C%22device_type_id%5C%22%3A13%2C%5C%22feed_pos%5C%22%3A0%7D%22%2C%22duration%22%3A68%2C%22upload_time%22%3A1702862537%7D
                              showType: 1
                              source:
                                iconUrl: >-
                                  https://wx.qlogo.cn/finderhead/ver_1/Eqf9VR6ArnSSAcFpMlIUW5AuTBpg2CZMPntNoeW5Un4RRVtD9EliboOT0VTJ7jqE9LzUvqwNRSeSwmbluyacxYw/132
                                title: <em class="highlight">人民日报</em>
                              title: 可爱！盘点2023年那些有趣的“显眼包”，一定要看到最后哦！
                              videoUrl: >-
                                https://findermp.video.qq.com/251/20302/stodownload?encfilekey=Cvvj5Ix3eewK0tHtibORqcsqchXNh0Gf3sJcaYqC2rQBTM1RO2c6hcib7hbN3s9Ng5aOrT5mOUvXfFy4sVlwVZmmNrgYuicnjQ0bG2mnk9SQVkLE6UckTPx3GhxaiaKxPrjL&bizid=1023&dotrans=0&hy=SH&idx=1&m=&upid=0&partscene=4&X-snsvideoflag=xW29&token=AxricY7RBHdVnQlzgG2jDJkiabetIWcNpyHT06K2TTEnmnvkGB6u6aeykRrFsvd6qlvmrW1jHOXdg
                              report_iteminfo_list_str: 14284646305856948573:feed:0
                          moreInfo:
                            moreID: '4313841664'
                          moreText: 更多
                          real_type: 18874368
                          resultType: 0
                          subType: 1
                          totalCount: 293
                          type: 86
                        - boxID: 0x80000000000-1-14156803322972604430
                          boxMergeValue: 4
                          boxPos: 10
                          boxPosMerge: 2
                          count: 1
                          items:
                            - dateTime: 7个月前
                              docID: '14156803322972604430'
                              duration: '00:55'
                              image: >-
                                http://wxapp.tc.qq.com/251/20304/stodownload?encfilekey=rjD5jyTuFrIpZ2ibE8T7YmwgiahniaXswqzAdVXxLSLDF6taNH5MhNx5ice88LoibicBjmGuzP2r5NcsicTdmB8WNG9wryWaHticibmmJaNFg3t1rffPCp9gver1taA&bizid=1023&dotrans=0&hy=SH&idx=1&m=&scene=0&token=6xykWLEnztKIzBicPuvgFxpECI8CSVyunJZN5qRnKLdaqcCYp6Uzsc0icwt7icJ55UR
                              imageData:
                                height: 1624
                                url: >-
                                  http://wxapp.tc.qq.com/251/20304/stodownload?encfilekey=rjD5jyTuFrIpZ2ibE8T7YmwgiahniaXswqzAdVXxLSLDF6taNH5MhNx5ice88LoibicBjmGuzP2r5NcsicTdmB8WNG9wryWaHticibmmJaNFg3t1rffPCp9gver1taA&bizid=1023&dotrans=0&hy=SH&idx=1&m=&scene=0&token=6xykWLEnztKIzBicPuvgFxpECI8CSVyunJZN5qRnKLdaqcCYp6Uzsc0icwt7icJ55UR
                                width: 1080
                              jumpInfo:
                                extInfo: >
                                  {"behavior":["report_feed_read","allow_pull_top","allow_infinite_top_pull"],"encryptedObjectId":"export/UzFfAgtgekIEAQAAAAAAwSsLWW54mgAAAAstQy6ubaLX4KHWvLEZgBPE2qMYGExfHt6HzNPgMIqKCjp4CFRQ4UeVvjI-KfDe","feedFocusChangeNotify":true,"feedNonceId":"15363446044240472021","getRelatedList":true,"reportExtraInfo":"{\"report_json\":\"\"}\n","reportScene":14,"requestScene":13,"sessionId":"CMiSyMf8kbnMxgEI4ZKAy_Tvwc7GAQjAsYD434aWzsYBCMSQhOuX643LxgEI3ZLMlZzE0J7GAQiOkOim3LPEu8QBCMmS2IHynpKsxgEI7pLsxs_2pKbGAQjqkcyVp7K32sQBCM6QzMzk_ImjxAEI65Ko6LWjmarGARC5l8DinZCDkOABKgzkurrmsJHml6XmiqUwADiAgICAgIACQAFQtZeZmA8."}
                                feedId: '14156803322972604430'
                                jumpType: 9
                              likeNum: 10万+
                              noPlayIcon: true
                              pubTime: 1687622466
                              reportId: 14156803322972604430:feed:0
                              report_extinfo_str: >-
                                %7B%22friend_like%22%3A0%2C%22item_tab%22%3A14%2C%22session_buffer%22%3A%22%7B%5C%22object_id%5C%22%3A14156803322972604430%2C%5C%22request_id%5C%22%3A16149922015637146553%2C%5C%22media_type%5C%22%3A0%2C%5C%22vid_len%5C%22%3A55%2C%5C%22create_time%5C%22%3A1687622466%2C%5C%22delivery_time%5C%22%3A1706083020%2C%5C%22comment_scene%5C%22%3A180%2C%5C%22delivery_scene%5C%22%3A76%2C%5C%22set_condition_flag%5C%22%3A51%2C%5C%22device_type_id%5C%22%3A13%2C%5C%22feed_pos%5C%22%3A0%7D%22%2C%22duration%22%3A55%2C%22upload_time%22%3A1687622466%7D
                              showType: 1
                              source:
                                iconUrl: >-
                                  https://wx.qlogo.cn/finderhead/ver_1/Eqf9VR6ArnSSAcFpMlIUW5AuTBpg2CZMPntNoeW5Un4RRVtD9EliboOT0VTJ7jqE9LzUvqwNRSeSwmbluyacxYw/132
                                title: <em class="highlight">人民日报</em>
                              title: >-
                                “中国人要把饭碗端在自己手里。”“牢牢守住18亿亩耕地红线。”今天是全国土地日，一起感悟习近平总书记对土地的深情。
                              videoUrl: >-
                                https://findermp.video.qq.com/251/20302/stodownload?encfilekey=Cvvj5Ix3eewK0tHtibORqcsqchXNh0Gf3sJcaYqC2rQBIViaPLRYR4L7VgsEdL5lBMEic1zAwbWpY1t68zyVqF1kT2YmomddJvg7kXiaoAwMa9FxKibU4EGcbtZRic2ykcjacP&bizid=1023&dotrans=0&hy=SH&idx=1&m=&partscene=4&X-snsvideoflag=xW29&token=cztXnd9GyrEsWrS4eJynZk47FDWNHKWQDAicZsKuLbGbVT3KXtfDY8giajNrKNJvvmwQuY6O848Xo
                              report_iteminfo_list_str: 14156803322972604430:feed:0
                          moreInfo:
                            moreID: '4313841664'
                          moreText: 更多
                          real_type: 18874368
                          resultType: 0
                          subType: 1
                          totalCount: 293
                          type: 86
                        - boxID: 0x80000000000-1-14292253643694803273
                          boxMergeValue: 4
                          boxPos: 11
                          boxPosMerge: 2
                          count: 1
                          items:
                            - dateTime: 26天前
                              docID: '14292253643694803273'
                              duration: '02:36'
                              image: >-
                                http://wxapp.tc.qq.com/251/20304/stodownload?encfilekey=rjD5jyTuFrIpZ2ibE8T7YmwgiahniaXswqzG1NY2bgA60ZxrIfONJkGian7fmCpkbxX3GibPKdbWtnDbZw5gqGicfurxYFtW2qwCZVb1wicn9KHjSS4G9S2bhJTtQ&bizid=1023&dotrans=0&hy=SH&idx=1&m=&scene=0&token=cztXnd9GyrGhE2iaHGOXDiaMyhQG00B2zZ5y0bBhtmxv7KibrUwp2GRj2QZz37ebqKn
                              imageData:
                                height: 1920
                                url: >-
                                  http://wxapp.tc.qq.com/251/20304/stodownload?encfilekey=rjD5jyTuFrIpZ2ibE8T7YmwgiahniaXswqzG1NY2bgA60ZxrIfONJkGian7fmCpkbxX3GibPKdbWtnDbZw5gqGicfurxYFtW2qwCZVb1wicn9KHjSS4G9S2bhJTtQ&bizid=1023&dotrans=0&hy=SH&idx=1&m=&scene=0&token=cztXnd9GyrGhE2iaHGOXDiaMyhQG00B2zZ5y0bBhtmxv7KibrUwp2GRj2QZz37ebqKn
                                width: 1080
                              jumpInfo:
                                extInfo: >
                                  {"behavior":["report_feed_read","allow_pull_top","allow_infinite_top_pull"],"encryptedObjectId":"export/UzFfAgtgekIEAQAAAAAAMf0uwIAl_QAAAAstQy6ubaLX4KHWvLEZgBPEnaEoP2JySMmFzNPgMIpZzW5t0IcS1JOcf0UV3MYV","feedFocusChangeNotify":true,"feedNonceId":"18392749158986613061","getRelatedList":true,"reportExtraInfo":"{\"report_json\":\"\"}\n","reportScene":14,"requestScene":13,"sessionId":"COGSgMv078HOxgEIwLGA-N-Gls7GAQjEkITrl-uNy8YBCN2SzJWcxNCexgEIjpDoptyzxLvEAQjJktiB8p6SrMYBCO6S7MbP9qSmxgEI6pHMlaeyt9rEAQjOkMzM5PyJo8QBCOuSqOi1o5mqxgEIgZCgr8eg97jDARC5l8DinZCDkOABKgzkurrmsJHml6XmiqUwADiAgICAgIACQAFQtZeZmA8."}
                                feedId: '14292253643694803273'
                                jumpType: 9
                              likeNum: 10万+
                              noPlayIcon: true
                              pubTime: 1703769402
                              reportId: 14292253643694803273:feed:0
                              report_extinfo_str: >-
                                %7B%22friend_like%22%3A0%2C%22item_tab%22%3A14%2C%22session_buffer%22%3A%22%7B%5C%22object_id%5C%22%3A14292253643694803273%2C%5C%22request_id%5C%22%3A16149922015637146553%2C%5C%22media_type%5C%22%3A0%2C%5C%22vid_len%5C%22%3A156%2C%5C%22create_time%5C%22%3A1703769402%2C%5C%22delivery_time%5C%22%3A1706083020%2C%5C%22comment_scene%5C%22%3A180%2C%5C%22delivery_scene%5C%22%3A76%2C%5C%22set_condition_flag%5C%22%3A51%2C%5C%22device_type_id%5C%22%3A13%2C%5C%22feed_pos%5C%22%3A0%7D%22%2C%22duration%22%3A156%2C%22upload_time%22%3A1703769402%7D
                              showType: 1
                              source:
                                iconUrl: >-
                                  https://wx.qlogo.cn/finderhead/ver_1/Eqf9VR6ArnSSAcFpMlIUW5AuTBpg2CZMPntNoeW5Un4RRVtD9EliboOT0VTJ7jqE9LzUvqwNRSeSwmbluyacxYw/132
                                title: <em class="highlight">人民日报</em>
                              title: >-
                                在2023年的日常里，总会被一些时刻治愈。带着善意和温暖，勇敢奔赴2024吧，愿我们都被世界温柔以待。
                              videoUrl: >-
                                https://findermp.video.qq.com/251/20302/stodownload?encfilekey=Cvvj5Ix3eewK0tHtibORqcsqchXNh0Gf3sJcaYqC2rQB3rKYydicL2IzMficRXmLniaF3VsB1xOGWgnM5OpJ1M4Ge7rEdK2hjoG9cQMiaLHtdk3I2UdiaGt5YNLibgn74TNwMlS&bizid=1023&dotrans=0&hy=SH&idx=1&m=&upid=0&partscene=4&X-snsvideoflag=xWT111&token=x5Y29zUxcibAicmfnZH1zhR0wvgnOexrYnW2sN5684V1ibjFTGnHdibW7eccicjovnchCIlIfGoMiaAJY
                              report_iteminfo_list_str: 14292253643694803273:feed:0
                          moreInfo:
                            moreID: '4313841664'
                          moreText: 更多
                          real_type: 18874368
                          resultType: 0
                          subType: 1
                          totalCount: 293
                          type: 86
                  direction: 2
                  experiment:
                    - key: mmsearch_finderclickhint_abtest
                      value: '0'
                  feedback:
                    isFromMixerMainSwap: 0
                  isBoxCardStyle: 1
                  isDivide: 0
                  isHomePage: 0
                  lang: zh_CN
                  offset: 9
                  pageNumber: 1
                  query: 人民日报
                  resultType: 0
                  ret: 0
                  searchID: '16149922015637146553'
                  timeStamp: 1706083020
          headers: {}
          x-apifox-name: 成功
      security: []
      x-apifox-folder: 基础API/视频号模块
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3475559/apis/api-144511330-run
components:
  schemas: {}
  securitySchemes: {}
servers:
  - url: http://218.78.116.24:10883
    description: 测试环境
security: []

```

# 创建视频号

## OpenAPI

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /gewe/v2/api/finder/createFinder:
    post:
      summary: 创建视频号
      deprecated: false
      description: ''
      tags:
        - 基础API/视频号模块
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
                nickName:
                  type: string
                  description: 视频号昵称
                headImg:
                  type: string
                  description: 视频号头像链接
                signature:
                  type: string
                  description: 视频号签名
                sex:
                  type: integer
                  description: 性别
              required:
                - appId
                - headImg
                - nickName
              x-apifox-orders:
                - appId
                - nickName
                - headImg
                - signature
                - sex
            example:
              appId: '{{appid}}'
              proxyIp: ''
              signature: 理智，清醒，知进退。
              headImg: >-
                https://wx.qlogo.cn/mmhead/ver_1/ZYUmcl1UNzyB2onM08Ij901TaUOLIjHj2UicK3XGDsjEWl4XgQN5IjodunHicBVsZiaZc1iaGCRfluAxkzyibbiau3WBfFj2nprzKp2KryicMjGIvDbWOQGmibwVK648a3o4A8hD/0
              nickName: 未来可期啊哈
              sex: 1
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
                      username:
                        type: string
                        description: 视频号的username
                      nickname:
                        type: string
                        description: 视频号的昵称
                      headUrl:
                        type: string
                        description: 头像
                      signature:
                        type: string
                        description: 简介
                      followFlag:
                        type: integer
                    required:
                      - username
                      - nickname
                      - headUrl
                      - signature
                      - followFlag
                    x-apifox-orders:
                      - username
                      - nickname
                      - headUrl
                      - signature
                      - followFlag
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
                      username: >-
                        v2_060000231003b20faec8c7e28811c4d5cc0ded37b0779c48c759a7446a87688c2774e5300c32@finder
                      nickname: 未来可期啊哈
                      headUrl: >-
                        http://wx.qlogo.cn/finderhead/AbruuZ3ILCkWiallQicn8kbXiafrvbTc6uMOYyC7WiaOzmle9GcMavFI3nSdMsAc916JoG9DRWAEHew/0
                      signature: 理智，清醒，知进退。
                      followFlag: 1
                '2':
                  summary: 异常示例
                  value:
                    ret: 500
                    msg: 创建视频号失败
                    data:
                      code: '-4002'
                      msg: 名字已被使用，请修改后再试。
          headers: {}
          x-apifox-name: 成功
      security: []
      x-apifox-folder: 基础API/视频号模块
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3475559/apis/api-144532615-run
components:
  schemas: {}
  securitySchemes: {}
servers:
  - url: http://218.78.116.24:10883
    description: 测试环境
security: []

```

# 同步私信消息

## OpenAPI

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /gewe/v2/api/finder/syncPrivateLetterMsg:
    post:
      summary: 同步私信消息
      deprecated: false
      description: ''
      tags:
        - 基础API/视频号模块
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
                keyBuff:
                  type: string
                  description: 首次传空，后续传接口返回的keyBuff
              required:
                - appId
              x-apifox-orders:
                - appId
                - keyBuff
            example:
              appId: '{{appid}}'
              proxyIp: ''
              keyBuff: ''
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
                      list:
                        type: array
                        items:
                          type: object
                          properties:
                            syncKeyType:
                              type: integer
                            itemType:
                              type: integer
                            content:
                              type: object
                              properties:
                                msg:
                                  type: object
                                  properties:
                                    MsgId:
                                      type: integer
                                      description: 消息ID
                                    FromUserName:
                                      type: object
                                      properties:
                                        string:
                                          type: string
                                      required:
                                        - string
                                      x-apifox-orders:
                                        - string
                                      description: 发送人的username
                                    ToUserName:
                                      type: object
                                      properties:
                                        string:
                                          type: string
                                      required:
                                        - string
                                      x-apifox-orders:
                                        - string
                                      description: 接收人的username
                                    MsgType:
                                      type: integer
                                      description: 消息类型
                                    Content:
                                      type: object
                                      properties:
                                        string:
                                          type: string
                                      required:
                                        - string
                                      x-apifox-orders:
                                        - string
                                      description: 消息内容
                                    Status:
                                      type: integer
                                    ImgStatus:
                                      type: integer
                                    ImgBuf:
                                      type: object
                                      properties:
                                        iLen:
                                          type: integer
                                      required:
                                        - iLen
                                      x-apifox-orders:
                                        - iLen
                                      description: 发送时间
                                    CreateTime:
                                      type: integer
                                    MsgSource:
                                      type: string
                                    NewMsgId:
                                      type: integer
                                      description: 消息newmsgid
                                    MsgSeq:
                                      type: integer
                                  required:
                                    - MsgId
                                    - FromUserName
                                    - ToUserName
                                    - MsgType
                                    - Content
                                    - Status
                                    - ImgStatus
                                    - ImgBuf
                                    - CreateTime
                                    - MsgSource
                                    - NewMsgId
                                    - MsgSeq
                                  x-apifox-orders:
                                    - MsgId
                                    - FromUserName
                                    - ToUserName
                                    - MsgType
                                    - Content
                                    - Status
                                    - ImgStatus
                                    - ImgBuf
                                    - CreateTime
                                    - MsgSource
                                    - NewMsgId
                                    - MsgSeq
                                msgSessionId:
                                  type: string
                                  description: 发私信消息时用到的sessionid
                                seq:
                                  type: integer
                                extinfo:
                                  type: string
                                isSender:
                                  type: integer
                                  description: 是不是自己发的消息，是：1  否：0
                              required:
                                - msg
                                - msgSessionId
                                - seq
                                - extinfo
                                - isSender
                              x-apifox-orders:
                                - msg
                                - msgSessionId
                                - seq
                                - extinfo
                                - isSender
                              description: 消息内容
                            subType:
                              type: integer
                              description: 消息类型
                          required:
                            - syncKeyType
                            - itemType
                            - content
                            - subType
                          x-apifox-orders:
                            - syncKeyType
                            - itemType
                            - content
                            - subType
                      keyBuff:
                        type: string
                        description: 翻页的key，请求翻页时会用到
                    required:
                      - list
                      - keyBuff
                    x-apifox-orders:
                      - list
                      - keyBuff
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
                  list:
                    - syncKeyType: 1
                      itemType: 1
                      content:
                        msg:
                          MsgId: 1
                          FromUserName:
                            string: wxid_0xsqb3o0tsvz22
                          ToUserName:
                            string: >-
                              v2_060000231003b20faec8c6e18f10c7d6c903ec3db0776955d3d97c6b329d6aa58693bcdb7ad1@finder
                          MsgType: 1
                          Content:
                            string: '1'
                          Status: 3
                          ImgStatus: 1
                          ImgBuf:
                            iLen: 0
                          CreateTime: 1706084719
                          MsgSource: <msgsource><pua>1</pua></msgsource>
                          NewMsgId: 5871873953492479000
                          MsgSeq: 1
                        msgSessionId: >-
                          ee06e16a186756394a271218d7dd31f65d3d6aa43dc02a1ec23758f588836d53@findermsg
                        seq: 1
                        extinfo: CAEQAQ==
                        isSender: 1
                      subType: 0
                    - syncKeyType: 5
                      itemType: 1
                      content:
                        msg:
                          MsgId: 2
                          FromUserName:
                            string: >-
                              v2_060000231003b20faec8c6e18f10c7d6c903ec3db0776955d3d97c6b329d6aa58693bcdb7ad1@finder
                          ToUserName:
                            string: >-
                              v2_060000231003b20faec8c7e28811c4d5cc0ded37b0779c48c759a7446a87688c2774e5300c32@finder
                          MsgType: 1
                          Content:
                            string: '12'
                          Status: 3
                          ImgStatus: 1
                          ImgBuf:
                            iLen: 0
                          CreateTime: 1706084785
                          MsgSource: >-
                            <msgsource><bizflag>0</bizflag><pua>1</pua></msgsource>
                          NewMsgId: 1054704077635816600
                          MsgSeq: 2
                        msgSessionId: >-
                          3eab1521919d4531c83a166faa56cf844737c4a295b127f3edcb68ed4375d049@findermsg
                        seq: 2
                        extinfo: CAEQAQ==
                        isSender: 0
                      subType: 2
                    - syncKeyType: 5
                      itemType: 1
                      content:
                        msg:
                          MsgId: 3
                          FromUserName:
                            string: >-
                              v2_060000231003b20faec8c7e28811c4d5cc0ded37b0779c48c759a7446a87688c2774e5300c32@finder
                          ToUserName:
                            string: >-
                              v2_060000231003b20faec8c6e18f10c7d6c903ec3db0776955d3d97c6b329d6aa58693bcdb7ad1@finder
                          MsgType: 1
                          Content:
                            string: 文本
                          Status: 3
                          ImgStatus: 1
                          ImgBuf:
                            iLen: 0
                          CreateTime: 1706084840
                          MsgSource: ''
                          NewMsgId: 243683914400108300
                          MsgSeq: 3
                        msgSessionId: >-
                          3eab1521919d4531c83a166faa56cf844737c4a295b127f3edcb68ed4375d049@findermsg
                        seq: 3
                        extinfo: CAIQAw==
                        isSender: 1
                      subType: 2
                    - syncKeyType: 5
                      itemType: 1
                      content:
                        msg:
                          MsgId: 4
                          FromUserName:
                            string: >-
                              v2_060000231003b20faec8c7e28811c4d5cc0ded37b0779c48c759a7446a87688c2774e5300c32@finder
                          ToUserName:
                            string: >-
                              v2_060000231003b20faec8c6e18f10c7d6c903ec3db0776955d3d97c6b329d6aa58693bcdb7ad1@finder
                          MsgType: 1
                          Content:
                            string: 文本
                          Status: 3
                          ImgStatus: 1
                          ImgBuf:
                            iLen: 0
                          CreateTime: 1706084898
                          MsgSource: ''
                          NewMsgId: 7648226390526412000
                          MsgSeq: 4
                        msgSessionId: >-
                          3eab1521919d4531c83a166faa56cf844737c4a295b127f3edcb68ed4375d049@findermsg
                        seq: 4
                        extinfo: CAIQAw==
                        isSender: 1
                      subType: 2
                    - syncKeyType: 5
                      itemType: 1
                      content:
                        msg:
                          MsgId: 5
                          FromUserName:
                            string: >-
                              v2_060000231003b20faec8c7e28811c4d5cc0ded37b0779c48c759a7446a87688c2774e5300c32@finder
                          ToUserName:
                            string: >-
                              v2_060000231003b20faec8c6e18f10c7d6c903ec3db0776955d3d97c6b329d6aa58693bcdb7ad1@finder
                          MsgType: 3
                          Content:
                            string: "<?xml version=\"1.0\"?>\n<msg>\n\t<img aeskey=\"38bd282fa5b21a42590269084f95975f\" encryver=\"1\" cdnthumbaeskey=\"38bd282fa5b21a42590269084f95975f\" cdnthumburl=\"3057020100044b30490201000204e49785f102032f5b0d0204e0689377020465b0cae1042436626432326532302d363466332d346135612d383238312d6636303061333033623762620204051438010201000405004c4c6d00\" cdnthumblength=\"1315\" cdnthumbheight=\"120\" cdnthumbwidth=\"120\" cdnmidheight=\"0\" cdnmidwidth=\"0\" cdnhdheight=\"0\" cdnhdwidth=\"0\" cdnmidimgurl=\"3057020100044b30490201000204e49785f102032f5b0d0204e0689377020465b0cae1042436626432326532302d363466332d346135612d383238312d6636303061333033623762620204051438010201000405004c4c6d00\" length=\"22001\" cdnbigimgurl=\"3057020100044b30490201000204e49785f102032f5b0d0204e0689377020465b0cae1042436626432326532302d363466332d346135612d383238312d6636303061333033623762620204051438010201000405004c4c6d00\" hdlength=\"1096\" md5=\"704de7ebbc107a51a4f0986253a6d3b6\" />\n\t<platform_signature></platform_signature>\n\t<imgdatahash></imgdatahash>\n</msg>\n"
                          Status: 3
                          ImgStatus: 2
                          ImgBuf:
                            iLen: 0
                          CreateTime: 1706085089
                          MsgSource: <msgsource><bizflag>0</bizflag></msgsource>
                          NewMsgId: 7744705344788547000
                          MsgSeq: 5
                        msgSessionId: >-
                          3eab1521919d4531c83a166faa56cf844737c4a295b127f3edcb68ed4375d049@findermsg
                        seq: 5
                        extinfo: CAIQAw==
                        isSender: 1
                      subType: 2
                  keyBuff: >-
                    CgQIARABCgQIAhAACgQIAxAACgQIBBAACgQIBRAFCgQIBhAACgQIBxAACgQICBAACgQICRAACgQIDBAAEAA=
          headers: {}
          x-apifox-name: 成功
      security: []
      x-apifox-folder: 基础API/视频号模块
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3475559/apis/api-144552901-run
components:
  schemas: {}
  securitySchemes: {}
servers:
  - url: http://218.78.116.24:10883
    description: 测试环境
security: []

```

# 根据id点赞

## OpenAPI

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /gewe/v2/api/finder/idFav:
    post:
      summary: 根据id点赞
      deprecated: false
      description: ''
      tags:
        - 基础API/视频号模块
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
                myUserName:
                  type: string
                  description: 自己的username
                opType:
                  type: integer
                  description: 1点赞 2取消点赞
                objectNonceId:
                  type: string
                  description: 视频号的objectNonceId
                sessionBuffer:
                  type: string
                  description: 视频号的sessionBuffer
                objectId:
                  type: integer
                  description: 视频号的ID
                toUserName:
                  type: string
                  description: 视频所有者userName
                myRoleType:
                  type: integer
                  description: 自己的roletype
              required:
                - appId
                - myUserName
                - opType
                - objectNonceId
                - sessionBuffer
                - objectId
                - toUserName
                - myRoleType
              x-apifox-orders:
                - appId
                - objectId
                - sessionBuffer
                - objectNonceId
                - opType
                - myUserName
                - myRoleType
                - toUserName
            example:
              appId: ''
              proxyIp: ''
              myUserName: ''
              opType: 1
              objectNonceId: '8507486792812551167_0_0_2_2_1719545315208098'
              sessionBuffer: >-
                eyJyZWNhbGxfdHlwZXMiOltdLCJkZWxpdmVyeV9zY2VuZSI6MiwiZGVsaXZlcnlfdGltZSI6MTcxOTU0NTMxNSwic2V0X2NvbmRpdGlvbl9mbGFnIjo5LCJyZWNhbGxfaW5kZXgiOltdLCJyZXF1ZXN0X2lkIjoxNzE5NTQ1MzE1MjA4MDk4LCJtZWRpYV90eXBlIjo0LCJ2aWRfbGVuIjoyLCJjcmVhdGVfdGltZSI6MTcxODMzNDg5MywicmVjYWxsX2luZm8iOltdLCJvZmxhZyI6MTY4MTgxOTIsImlkYyI6MywiZGV2aWNlX3R5cGVfaWQiOjEzLCJkZXZpY2VfcGxhdGZvcm0iOiJpUGFkMTEsMyIsImZlZWRfcG9zIjowLCJjbGllbnRfcmVwb3J0X2J1ZmYiOiJ7XCJpZl9zcGxpdF9zY3JlZW5faXBhZFwiOjAsXCJlbnRlclNvdXJjZUluZm9cIjpcIntcXFwiZmluZGVydXNlcm5hbWVcXFwiOlxcXCJcXFwiLFxcXCJmZWVkaWRcXFwiOlxcXCJcXFwifVwiLFwiZXh0cmFpbmZvXCI6XCJ7XFxcInJlZ2NvdW50cnlcXFwiOlxcXCJDTlxcXCJ9XCIsXCJzZXNzaW9uSWRcIjpcIlNwbGl0Vmlld0VtcHR5Vmlld0NvbnRyb2xsZXJfMTcxOTU0NTMwNjU5NiMkMF8xNzE5NTQ1MjkzOTYwI1wiLFwianVtcElkXCI6e1widHJhY2VpZFwiOlwiXCIsXCJzb3VyY2VpZFwiOlwiXCJ9fSIsIm9iamVjdF9pZCI6MTQ0MTQ0Mzc4MzUwMTE1MjkwMDcsImZpbmRlcl91aW4iOjEzMTA0ODA1MzY5MjE2NzMyLCJnZW9oYXNoIjozMzc3Njk5NzIwNTI3ODcyLCJlbnRyYW5jZV9zY2VuZSI6MiwiY2FyZF90eXBlIjozLCJleHB0X2ZsYWciOjg4Nzg3OTU1LCJ1c2VyX21vZGVsX2ZsYWciOjgsImlzX2ZyaWVuZCI6dHJ1ZSwiY3R4X2lkIjoiMi0zLTMyLWYxNjU5NWU2YjhlYmVjZjVhNDRhZGMzZWY1NGQzYzdhMTcxOTU0NTMxMTcyMiIsImFkX2ZsYWciOjQsImVyaWwiOltdLCJwZ2tleXMiOltdLCJzY2lkIjoiODA2MmY0NTQtMzRmZS0xMWVmLTkxOWUtZGYyYjg4ZGI2N2M5IiwiY29tbWVudF92ZXIiOjE3MTk0ODE2NDJ9
              objectId: 14414437835011529000
              toUserName: >-
                v2_060000231003b20faec8c7e08f10c1d4c803ef36b077bc0b9fb41ae2efc82c20ba5fb68f838a@finder
              myRoleType: 3
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
              example:
                ret: 200
                msg: 操作成功
          headers: {}
          x-apifox-name: 成功
      security: []
      x-apifox-folder: 基础API/视频号模块
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3475559/apis/api-189454588-run
components:
  schemas: {}
  securitySchemes: {}
servers:
  - url: http://218.78.116.24:10883
    description: 测试环境
security: []

```

# 根据id点小红心

## OpenAPI

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /gewe/v2/api/finder/idLike:
    post:
      summary: 根据id点小红心
      deprecated: false
      description: ''
      tags:
        - 基础API/视频号模块
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
                objectId:
                  type: integer
                  description: 视频号的objectId
                sessionBuffer:
                  type: string
                  description: 视频号的sessionBuffer
                objectNonceId:
                  type: string
                  description: 视频号的objectNonceId
                opType:
                  type: integer
                  description: 3喜欢  4不喜欢
                myUserName:
                  type: string
                  description: 自己的username
                myRoleType:
                  type: integer
                  description: 自己的roletype
                toUserName:
                  type: string
                  description: 视频所有者userName
              required:
                - appId
                - myUserName
                - opType
                - objectId
                - myRoleType
                - objectNonceId
                - toUserName
              x-apifox-orders:
                - appId
                - objectId
                - sessionBuffer
                - objectNonceId
                - opType
                - myUserName
                - myRoleType
                - toUserName
            example:
              appId: ''
              proxyIp: ''
              myUserName: ''
              opType: 3
              objectNonceId: '8507486792812551167_0_0_2_2_1719545315208098'
              sessionBuffer: >-
                eyJyZWNhbGxfdHlwZXMiOltdLCJkZWxpdmVyeV9zY2VuZSI6MiwiZGVsaXZlcnlfdGltZSI6MTcxOTU0NTMxNSwic2V0X2NvbmRpdGlvbl9mbGFnIjo5LCJyZWNhbGxfaW5kZXgiOltdLCJyZXF1ZXN0X2lkIjoxNzE5NTQ1MzE1MjA4MDk4LCJtZWRpYV90eXBlIjo0LCJ2aWRfbGVuIjoyLCJjcmVhdGVfdGltZSI6MTcxODMzNDg5MywicmVjYWxsX2luZm8iOltdLCJvZmxhZyI6MTY4MTgxOTIsImlkYyI6MywiZGV2aWNlX3R5cGVfaWQiOjEzLCJkZXZpY2VfcGxhdGZvcm0iOiJpUGFkMTEsMyIsImZlZWRfcG9zIjowLCJjbGllbnRfcmVwb3J0X2J1ZmYiOiJ7XCJpZl9zcGxpdF9zY3JlZW5faXBhZFwiOjAsXCJlbnRlclNvdXJjZUluZm9cIjpcIntcXFwiZmluZGVydXNlcm5hbWVcXFwiOlxcXCJcXFwiLFxcXCJmZWVkaWRcXFwiOlxcXCJcXFwifVwiLFwiZXh0cmFpbmZvXCI6XCJ7XFxcInJlZ2NvdW50cnlcXFwiOlxcXCJDTlxcXCJ9XCIsXCJzZXNzaW9uSWRcIjpcIlNwbGl0Vmlld0VtcHR5Vmlld0NvbnRyb2xsZXJfMTcxOTU0NTMwNjU5NiMkMF8xNzE5NTQ1MjkzOTYwI1wiLFwianVtcElkXCI6e1widHJhY2VpZFwiOlwiXCIsXCJzb3VyY2VpZFwiOlwiXCJ9fSIsIm9iamVjdF9pZCI6MTQ0MTQ0Mzc4MzUwMTE1MjkwMDcsImZpbmRlcl91aW4iOjEzMTA0ODA1MzY5MjE2NzMyLCJnZW9oYXNoIjozMzc3Njk5NzIwNTI3ODcyLCJlbnRyYW5jZV9zY2VuZSI6MiwiY2FyZF90eXBlIjozLCJleHB0X2ZsYWciOjg4Nzg3OTU1LCJ1c2VyX21vZGVsX2ZsYWciOjgsImlzX2ZyaWVuZCI6dHJ1ZSwiY3R4X2lkIjoiMi0zLTMyLWYxNjU5NWU2YjhlYmVjZjVhNDRhZGMzZWY1NGQzYzdhMTcxOTU0NTMxMTcyMiIsImFkX2ZsYWciOjQsImVyaWwiOltdLCJwZ2tleXMiOltdLCJzY2lkIjoiODA2MmY0NTQtMzRmZS0xMWVmLTkxOWUtZGYyYjg4ZGI2N2M5IiwiY29tbWVudF92ZXIiOjE3MTk0ODE2NDJ9
              objectId: 14414437835011529000
              toUserName: >-
                v2_060000231003b20faec8c7e08f10c1d4c803ef36b077bc0b9fb41ae2efc82c20ba5fb68f838a@finder
              myRoleType: 3
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
              example:
                ret: 200
                msg: 操作成功
          headers: {}
          x-apifox-name: 成功
      security: []
      x-apifox-folder: 基础API/视频号模块
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3475559/apis/api-189454620-run
components:
  schemas: {}
  securitySchemes: {}
servers:
  - url: http://218.78.116.24:10883
    description: 测试环境
security: []

```

# 获取我的视频号信息

## OpenAPI

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /gewe/v2/api/finder/getProfile:
    post:
      summary: 获取我的视频号信息
      deprecated: false
      description: ''
      tags:
        - 基础API/视频号模块
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
              required:
                - appId
              x-apifox-orders:
                - appId
            example:
              appId: '{{appid}}'
              proxyIp: ''
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
                      signatureMaxLength:
                        type: integer
                        description: 简介文字最大长度
                      nicknameMinLength:
                        type: integer
                        description: 昵称文字最小长度
                      nicknameMaxLength:
                        type: integer
                        description: 昵称文字最大长度
                      userNoFinder:
                        type: integer
                      purchasedTotalCount:
                        type: integer
                      privacySetting:
                        type: object
                        properties:
                          exportJumpLink:
                            type: string
                        required:
                          - exportJumpLink
                        x-apifox-orders:
                          - exportJumpLink
                        description: 隐私设置
                      aliasInfo:
                        type: array
                        items:
                          type: object
                          properties:
                            nickname:
                              type: string
                              description: 昵称
                            headImgUrl:
                              type: string
                              description: 头像
                            roleType:
                              type: integer
                              description: 身份类型，微信身份:1  视频号身份:3
                          required:
                            - nickname
                            - headImgUrl
                            - roleType
                          x-apifox-orders:
                            - nickname
                            - headImgUrl
                            - roleType
                        description: 身份信息
                      currentAliasRoleType:
                        type: integer
                        description: 当前选择的身份类型
                      nextAliasModAvailableTime:
                        type: integer
                      actionWording:
                        type: object
                        properties: {}
                        x-apifox-orders: []
                      userFlag:
                        type: integer
                      mainFinderUsername:
                        type: string
                        description: 我的视频号username【重要】
                    required:
                      - mainFinderUsername
                      - signatureMaxLength
                      - nicknameMinLength
                      - nicknameMaxLength
                      - userNoFinder
                      - purchasedTotalCount
                      - privacySetting
                      - aliasInfo
                      - currentAliasRoleType
                      - nextAliasModAvailableTime
                      - actionWording
                      - userFlag
                    x-apifox-orders:
                      - signatureMaxLength
                      - nicknameMinLength
                      - nicknameMaxLength
                      - userNoFinder
                      - purchasedTotalCount
                      - privacySetting
                      - aliasInfo
                      - currentAliasRoleType
                      - nextAliasModAvailableTime
                      - actionWording
                      - userFlag
                      - mainFinderUsername
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
                  mainFinderUsername: >-
                    v2_060000231003b20faec8c7e28811c4d5cc0ded37b0779c48c759a7446a87688c2774e5300c32@finder
                  signatureMaxLength: 400
                  nicknameMinLength: 2
                  nicknameMaxLength: 30
                  userNoFinder: 0
                  purchasedTotalCount: 0
                  privacySetting:
                    exportJumpLink: >-
                      https://channels.weixin.qq.com/pandora/pages/biz-binding/exportdata.html
                  aliasInfo:
                    - nickname: G
                      headImgUrl: >-
                        http://wx.qlogo.cn/mmhead/AbruuZ3ILCmPOG26jEOF7VXZnhYfpz9NQ0mhFrvicr7BoFX6fVbtibLKVjzPaHlUMeH4ialliaxkNH8/0
                      roleType: 1
                    - nickname: 未来可期啊哈
                      headImgUrl: >-
                        http://wx.qlogo.cn/finderhead/AbruuZ3ILCkWiallQicn8kbXiafrvbTc6uMOYyC7WiaOzmle9GcMavFI3nSdMsAc916JoG9DRWAEHew/0
                      roleType: 3
                  currentAliasRoleType: 1
                  nextAliasModAvailableTime: 0
                  actionWording: {}
                  userFlag: 5
          headers: {}
          x-apifox-name: 成功
      security: []
      x-apifox-folder: 基础API/视频号模块
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3475559/apis/api-144530919-run
components:
  schemas: {}
  securitySchemes: {}
servers:
  - url: http://218.78.116.24:10883
    description: 测试环境
security: []

```

# 修改我的视频号信息

## OpenAPI

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /gewe/v2/api/finder/updateProfile:
    post:
      summary: 修改我的视频号信息
      deprecated: false
      description: ''
      tags:
        - 基础API/视频号模块
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
                nickName:
                  type: string
                  description: 昵称
                headImg:
                  type: string
                  description: 头像链接
                signature:
                  type: string
                  description: 签名
                sex:
                  type: integer
                  description: 性别
                country:
                  type: string
                  description: 国家
                province:
                  type: string
                  description: 省份
                city:
                  type: string
                  description: 城市
                myUserName:
                  type: string
                  description: 自己的username，可通过获取视频号信息接口获取
                myRoleType:
                  type: integer
                  description: 自己的roletype，可通过获取视频号信息接口获取
              required:
                - appId
                - myRoleType
                - myUserName
              x-apifox-orders:
                - appId
                - nickName
                - headImg
                - signature
                - sex
                - country
                - province
                - city
                - myUserName
                - myRoleType
            example:
              appId: '{{appid}}'
              proxyIp: ''
              signature: 理智，清醒，知进退。
              headImg: >-
                https://wx.qlogo.cn/mmhead/ver_1/ZYUmcl1UNzyB2onM08Ij901TaUOLIjHj2UicK3XGDsjEWl4XgQN5IjodunHicBVsZiaZc1iaGCRfluAxkzyibbiau3WBfFj2nprzKp2KryicMjGIvDbWOQGmibwVK648a3o4A8hD/0
              nickName: 未来可期啊哈
              sex: 1
              city: Nanjing
              province: Jiangsu
              country: CN
              myRoleType: 3
              myUserName: >-
                v2_060000231003b20faec8c7e28811c4d5cc0ded37b0779c48c759a7446a87688c2774e5300c32@finder
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
              examples:
                '1':
                  summary: 成功示例
                  value:
                    ret: 200
                    msg: 操作成功
                '2':
                  summary: 异常示例
                  value:
                    ret: 500
                    msg: 创建视频号失败
                    data:
                      code: '-4002'
                      msg: 名字已被使用，请修改后再试。
          headers: {}
          x-apifox-name: 成功
      security: []
      x-apifox-folder: 基础API/视频号模块
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3475559/apis/api-144594614-run
components:
  schemas: {}
  securitySchemes: {}
servers:
  - url: http://218.78.116.24:10883
    description: 测试环境
security: []

```

# 发送视频号消息

## OpenAPI

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /gewe/v2/api/message/sendFinderMsg:
    post:
      summary: 发送视频号消息
      deprecated: false
      description: ''
      tags:
        - 基础API/视频号模块
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
                toWxid:
                  type: string
                  description: 接收人wxid
                id:
                  type: integer
                  description: 视频信息id
                username:
                  type: string
                  description: 视频发布者username
                nickname:
                  type: string
                  description: 视频发布者昵称
                headUrl:
                  type: string
                  description: 视频发布者头像
                nonceId:
                  type: string
                  description: 视频nonceId
                mediaType:
                  type: string
                  description: 视频类型
                width:
                  type: string
                  description: 视频宽度
                height:
                  type: string
                  description: 视频高度
                url:
                  type: string
                  description: url
                thumbUrl:
                  type: string
                  description: thumbUrl
                thumbUrlToken:
                  type: string
                  description: thumbUrlToken
                description:
                  type: string
                  description: 视频描述
                videoPlayLen:
                  type: string
                  description: 播放时长
              required:
                - appId
                - toWxid
                - id
                - username
                - nickname
                - headUrl
                - nonceId
                - mediaType
                - width
                - height
                - url
                - thumbUrl
                - thumbUrlToken
                - description
                - videoPlayLen
              x-apifox-orders:
                - appId
                - toWxid
                - id
                - username
                - nickname
                - headUrl
                - nonceId
                - mediaType
                - width
                - height
                - url
                - thumbUrl
                - thumbUrlToken
                - description
                - videoPlayLen
            example:
              appId: '{{appid}}'
              proxyIp: ''
              toWxid: ''
              id: 14414437835011529000
              username: >-
                v2_060000231003b20faec8c7e08f10c1d4c803ef36b077bc0b9fb41ae2efc82c20ba5fb68f838a@finder
              nickname: 爱德华9813
              headUrl: >-
                https://wx.qlogo.cn/finderhead/ver_1/nlibhBXsVzorXqOtGniaqibbThkBtq0RiaILNqtOBcQQm1e16E5WrWF2uFQUDQiaglw0IavDb4eHGPPwp1c1tAF8aZkybLpBVdibRTocbVVeZAD6o/0
              nonceId: '8507486792812551167_0_0_2_2_1724662626395281'
              mediaType: '4'
              width: '1000'
              height: '2000'
              url: >-
                http://wxapp.tc.qq.com/251/20302/stodownload?encfilekey=Cvvj5Ix3eexKX1zo1IZZBrQomawdVfSQH1uu2U31EqFp6r4vicWibDJB8iciaEBdZuUC17CsQYbsbayvsu3MXT3QSE4ibicgB2nKU5TAFpxnZBeG3fJrjFN4xxlW1mN0uWtZa5YrwN5ib53OqP497WNcqYtyicvcib2FlISGKIXz6zGB74y4&a=1&dotrans=0&hy=SH&idx=1&m=d0d78a9d4690ba3f16e9b4a8c0192845&uzid=2
              thumbUrl: >-
                http://wxapp.tc.qq.com/251/20350/stodownload?encfilekey=Cvvj5Ix3eexKX1zo1IZZBrQomawdVfSQH1uu2U31EqEMP8IAeiakw55yiaLw4LU7ja4f0oVVPzPEQdGG9LDBr5o7CicibFocrhKFj266sHef2078toMU9tDj17fIvtJgXT9ZU1By0a0L0RE1J2AleALLHCsQOz0eNbTaD5Bbic3CEwZY&dotrans=0&hy=SH&idx=1&m=0babaadbda6c96767df974ce651bc42f&picformat=200
              thumbUrlToken: >-
                &token=oA9SZ4icv8It97yyPy38aPOBXibibl3IO9EqLX4chttFyw4ZS02VEgicB6P44BQKVQoQ4uUribzV520RxiaE0aPwM5LPqE6UZyyqtvhLeRl4Hsicib8
              description: '123321#321hh #123哈哈'
              videoPlayLen: '2'
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
      x-apifox-folder: 基础API/视频号模块
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3475559/apis/api-210852661-run
components:
  schemas: {}
  securitySchemes: {}
servers:
  - url: http://218.78.116.24:10883
    description: 测试环境
security: []

```

# 发送视频号朋友圈

## OpenAPI

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /gewe/v2/api/sns/sendFinderSns:
    post:
      summary: 发送视频号朋友圈
      deprecated: false
      description: ''
      tags:
        - 基础API/视频号模块
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
                allowWxIds:
                  type: array
                  items:
                    type: string
                  title: 允许谁看
                atWxIds:
                  type: array
                  items:
                    type: string
                  title: 提醒谁看
                disableWxIds:
                  type: array
                  items:
                    type: string
                  title: 不给谁看
                id:
                  type: integer
                  title: 视频id
                username:
                  type: string
                  title: 视频作者username
                nickname:
                  type: string
                  title: 视频作者昵称
                headUrl:
                  type: string
                  title: 作者头像
                nonceId:
                  type: string
                  title: nonceId
                mediaType:
                  type: string
                  title: 类型
                width:
                  type: string
                  title: 宽度
                height:
                  type: string
                  title: 高度
                url:
                  type: string
                thumbUrl:
                  type: string
                thumbUrlToken:
                  type: string
                description:
                  type: string
                videoPlayLen:
                  type: string
                  title: 播放时长
              required:
                - appId
                - allowWxIds
                - atWxIds
                - disableWxIds
                - id
                - username
                - nickname
                - headUrl
                - nonceId
                - mediaType
                - width
                - height
                - url
                - thumbUrl
                - thumbUrlToken
                - description
                - videoPlayLen
              x-apifox-orders:
                - appId
                - allowWxIds
                - atWxIds
                - disableWxIds
                - id
                - username
                - nickname
                - headUrl
                - nonceId
                - mediaType
                - width
                - height
                - url
                - thumbUrl
                - thumbUrlToken
                - description
                - videoPlayLen
            example:
              appId: '{{appid}}'
              proxyIp: ''
              allowWxIds: []
              atWxIds: []
              disableWxIds: []
              id: 14414437835011529000
              username: >-
                v2_060000231003b20faec8c7e08f10c1d4c803ef36b077bc0b9fb41ae2efc82c20ba5fb68f838a@finder
              nickname: 爱德华9813
              headUrl: >-
                https://wx.qlogo.cn/finderhead/ver_1/nlibhBXsVzorXqOtGniaqibbThkBtq0RiaILNqtOBcQQm1e16E5WrWF2uFQUDQiaglw0IavDb4eHGPPwp1c1tAF8aZkybLpBVdibRTocbVVeZAD6o/0
              nonceId: '8507486792812551167_0_0_2_2_1724662626395281'
              mediaType: '4'
              width: '1000'
              height: '2000'
              url: >-
                http://wxapp.tc.qq.com/251/20302/stodownload?encfilekey=Cvvj5Ix3eexKX1zo1IZZBrQomawdVfSQH1uu2U31EqFp6r4vicWibDJB8iciaEBdZuUC17CsQYbsbayvsu3MXT3QSE4ibicgB2nKU5TAFpxnZBeG3fJrjFN4xxlW1mN0uWtZa5YrwN5ib53OqP497WNcqYtyicvcib2FlISGKIXz6zGB74y4&a=1&dotrans=0&hy=SH&idx=1&m=d0d78a9d4690ba3f16e9b4a8c0192845&uzid=2
              thumbUrl: >-
                http://wxapp.tc.qq.com/251/20350/stodownload?encfilekey=Cvvj5Ix3eexKX1zo1IZZBrQomawdVfSQH1uu2U31EqEMP8IAeiakw55yiaLw4LU7ja4f0oVVPzPEQdGG9LDBr5o7CicibFocrhKFj266sHef2078toMU9tDj17fIvtJgXT9ZU1By0a0L0RE1J2AleALLHCsQOz0eNbTaD5Bbic3CEwZY&dotrans=0&hy=SH&idx=1&m=0babaadbda6c96767df974ce651bc42f&picformat=200
              thumbUrlToken: >-
                &token=oA9SZ4icv8It97yyPy38aPOBXibibl3IO9EqLX4chttFyw4ZS02VEgicB6P44BQKVQoQ4uUribzV520RxiaE0aPwM5LPqE6UZyyqtvhLeRl4Hsicib8
              description: '123321#321hh #123哈哈'
              videoPlayLen: '2'
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
      x-apifox-folder: 基础API/视频号模块
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3475559/apis/api-212050672-run
components:
  schemas: {}
  securitySchemes: {}
servers:
  - url: http://218.78.116.24:10883
    description: 测试环境
security: []

```

# 获取私信人信息

## OpenAPI

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /gewe/v2/api/finder/contactList:
    post:
      summary: 获取私信人信息
      deprecated: false
      description: ''
      tags:
        - 基础API/视频号模块
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
                myUserName:
                  type: string
                  description: 自己的username
                myRoleType:
                  type: integer
                  description: 自己的roletype
                queryInfo:
                  type: string
                  description: 联系人的username
              required:
                - appId
                - myUserName
                - myRoleType
                - queryInfo
              x-apifox-orders:
                - appId
                - myUserName
                - myRoleType
                - queryInfo
            example:
              appId: '{{appid}}'
              proxyIp: ''
              myUserName: >-
                v2_060000231003b20faec8c7e28811c4d5cc0ded37b0779c48c759a7446a87688c2774e5300c32@finder
              queryInfo: >-
                fv1_f81ac363407fa7a7c4728898ba5a2581c9627330378aabb49d783582bb7120d1@findermsgstranger
              myRoleType: 3
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
                        username:
                          type: string
                          description: 联系人的username
                        nickname:
                          type: string
                          description: 昵称
                        headUrl:
                          type: string
                          description: 头像
                        signature:
                          type: string
                          description: 简介
                        extInfo:
                          type: object
                          properties:
                            country:
                              type: string
                              description: 国家
                            province:
                              type: string
                              description: 省份
                            city:
                              type: string
                              description: 城市
                            sex:
                              type: integer
                              description: 性别
                          required:
                            - country
                            - province
                            - city
                            - sex
                          x-apifox-orders:
                            - country
                            - province
                            - city
                            - sex
                          description: 扩展信息
                        msgInfo:
                          type: object
                          properties:
                            msgUsername:
                              type: string
                            sessionId:
                              type: string
                              description: 发送私信时用到的sessionid
                          required:
                            - msgUsername
                            - sessionId
                          x-apifox-orders:
                            - msgUsername
                            - sessionId
                        wxUsernameV5:
                          type: string
                      x-apifox-orders:
                        - username
                        - nickname
                        - headUrl
                        - signature
                        - extInfo
                        - msgInfo
                        - wxUsernameV5
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
                  - username: >-
                      fv1_f81ac363407fa7a7c4728898ba5a2581c9627330378aabb49d783582bb7120d1@findermsgstranger
                    nickname: Ashley
                    headUrl: >-
                      https://wx.qlogo.cn/mmhead/ver_1/aYdhjJAmMNckmfOXbjpTDSaXyehkS3sIyQjqSBNvP81eibcokmMNjqMlx6fHRvibiaKyJv17TkyJ3NelpIAQ9mDic4MKj6uSPibGbNZ3StM9JeZc/132
                    signature: 山林不向四季起誓 枯荣随缘。
                    extInfo:
                      country: AD
                      province: ''
                      city: ''
                      sex: 2
                    msgInfo:
                      msgUsername: >-
                        fv1_f81ac363407fa7a7c4728898ba5a2581c9627330378aabb49d783582bb7120d1@findermsgstranger
                      sessionId: >-
                        f81ac363407fa7a7c4728898ba5a2581c9627330378aabb49d783582bb7120d1@findermsg
                    wxUsernameV5: >-
                      v5_020b0a1661040100000000002c4826ef09fc3d000000b1afa7d8728e3dd43ef4317a780e33c2de646dc7a8e59366e1f748ba6dc68191ea033d9b01761a6f3699af1758780bb837eb84d3fbb03e29575db6b2ca93526f29c3cda5df226312e78b3efc9e@stranger
          headers: {}
          x-apifox-name: 成功
      security: []
      x-apifox-folder: 基础API/视频号模块
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3475559/apis/api-144596478-run
components:
  schemas: {}
  securitySchemes: {}
servers:
  - url: http://218.78.116.24:10883
    description: 测试环境
security: []

```

# 发私信文本消息

## OpenAPI

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /gewe/v2/api/finder/postPrivateLetter:
    post:
      summary: 发私信文本消息
      deprecated: false
      description: ''
      tags:
        - 基础API/视频号模块
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
                content:
                  type: string
                  description: 私信内容
                toUserName:
                  type: string
                  description: 接收方的username
                myUserName:
                  type: string
                  description: 自己的usenrame
                msgSessionId:
                  type: string
                  description: 可通过/contactList接口获取
              required:
                - appId
                - content
                - msgSessionId
                - myUserName
                - toUserName
              x-apifox-orders:
                - appId
                - content
                - toUserName
                - myUserName
                - msgSessionId
            example:
              appId: '{{appid}}'
              proxyIp: ''
              content: 文本
              msgSessionId: >-
                3eab1521919d4531c83a166faa56cf844737c4a295b127f3edcb68ed4375d049@findermsg
              myUserName: >-
                v2_060000231003b20faec8c7e28811c4d5cc0ded37b0779c48c759a7446a87688c2774e5300c32@finder
              toUserName: >-
                v2_060000231003b20faec8c6e18f10c7d6c903ec3db0776955d3d97c6b329d6aa58693bcdb7ad1@finder
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
                      newMsgId:
                        type: integer
                        description: 消息的newmsgid
                    required:
                      - newMsgId
                    x-apifox-orders:
                      - newMsgId
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
                  newMsgId: 243683914400108300
          headers: {}
          x-apifox-name: 成功
      security: []
      x-apifox-folder: 基础API/视频号模块
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3475559/apis/api-144528559-run
components:
  schemas: {}
  securitySchemes: {}
servers:
  - url: http://218.78.116.24:10883
    description: 测试环境
security: []

```

# 发私信文本消息

## OpenAPI

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /gewe/v2/api/finder/postPrivateLetter:
    post:
      summary: 发私信文本消息
      deprecated: false
      description: ''
      tags:
        - 基础API/视频号模块
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
                content:
                  type: string
                  description: 私信内容
                toUserName:
                  type: string
                  description: 接收方的username
                myUserName:
                  type: string
                  description: 自己的usenrame
                msgSessionId:
                  type: string
                  description: 可通过/contactList接口获取
              required:
                - appId
                - content
                - msgSessionId
                - myUserName
                - toUserName
              x-apifox-orders:
                - appId
                - content
                - toUserName
                - myUserName
                - msgSessionId
            example:
              appId: '{{appid}}'
              proxyIp: ''
              content: 文本
              msgSessionId: >-
                3eab1521919d4531c83a166faa56cf844737c4a295b127f3edcb68ed4375d049@findermsg
              myUserName: >-
                v2_060000231003b20faec8c7e28811c4d5cc0ded37b0779c48c759a7446a87688c2774e5300c32@finder
              toUserName: >-
                v2_060000231003b20faec8c6e18f10c7d6c903ec3db0776955d3d97c6b329d6aa58693bcdb7ad1@finder
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
                      newMsgId:
                        type: integer
                        description: 消息的newmsgid
                    required:
                      - newMsgId
                    x-apifox-orders:
                      - newMsgId
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
                  newMsgId: 243683914400108300
          headers: {}
          x-apifox-name: 成功
      security: []
      x-apifox-folder: 基础API/视频号模块
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3475559/apis/api-144528559-run
components:
  schemas: {}
  securitySchemes: {}
servers:
  - url: http://218.78.116.24:10883
    description: 测试环境
security: []

```

# 扫码关注

## OpenAPI

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /gewe/v2/api/finder/scanFollow:
    post:
      summary: 扫码关注
      deprecated: false
      description: ''
      tags:
        - 基础API/视频号模块
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
                proxyIp:
                  type: string
                myUserName:
                  type: string
                  description: 当前用户的userName
                myRoleType:
                  type: integer
                  description: 身份类型 1：微信 3：视频号
                qrContent:
                  type: string
                  description: 内容信息 二维码链接或对方的userName
                objectId:
                  type: string
                  description: 如果qrContent 为对方userName 则参数必传，内容从用户主页获取
                objectNonceId:
                  type: string
                  description: 如果qrContent 为对方userName 则参数必传，内容从用户主页获取
              required:
                - appId
                - proxyIp
                - myUserName
                - myRoleType
                - qrContent
                - objectId
                - objectNonceId
              x-apifox-orders:
                - appId
                - proxyIp
                - myUserName
                - myRoleType
                - qrContent
                - objectId
                - objectNonceId
            example:
              appId: '{{appid}}'
              proxyIp: ''
              myUserName: v2_060000231003b**8c759a7446a87688c2774e5300c32@finder
              myRoleType: 3
              qrContent: v2_060000231003**465d77bc1e1c959b96ccee6e@finder
              objectId: 144487526**8757
              objectNonceId: 16839900**8113015869
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
                      username:
                        type: string
                        description: 对方的username
                      nickname:
                        type: string
                        description: 昵称
                      headUrl:
                        type: string
                        description: 头像
                      signature:
                        type: string
                        description: 简介
                      followFlag:
                        type: integer
                      authInfo:
                        type: object
                        properties: {}
                        x-apifox-orders: []
                      coverImgUrl:
                        type: string
                      spamStatus:
                        type: integer
                      extFlag:
                        type: integer
                      extInfo:
                        type: object
                        properties:
                          sex:
                            type: integer
                            description: 性别
                        required:
                          - sex
                        x-apifox-orders:
                          - sex
                      liveStatus:
                        type: integer
                      liveCoverImgUrl:
                        type: string
                      liveInfo:
                        type: object
                        properties:
                          anchorStatusFlag:
                            type: integer
                          switchFlag:
                            type: integer
                          lotterySetting:
                            type: object
                            properties:
                              settingFlag:
                                type: integer
                              attendType:
                                type: integer
                            required:
                              - settingFlag
                              - attendType
                            x-apifox-orders:
                              - settingFlag
                              - attendType
                        required:
                          - anchorStatusFlag
                          - switchFlag
                          - lotterySetting
                        x-apifox-orders:
                          - anchorStatusFlag
                          - switchFlag
                          - lotterySetting
                      status:
                        type: integer
                    required:
                      - username
                      - nickname
                      - headUrl
                      - signature
                      - followFlag
                      - authInfo
                      - coverImgUrl
                      - spamStatus
                      - extFlag
                      - extInfo
                      - liveStatus
                      - liveCoverImgUrl
                      - liveInfo
                      - status
                    x-apifox-orders:
                      - username
                      - nickname
                      - headUrl
                      - signature
                      - followFlag
                      - authInfo
                      - coverImgUrl
                      - spamStatus
                      - extFlag
                      - extInfo
                      - liveStatus
                      - liveCoverImgUrl
                      - liveInfo
                      - status
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
                  username: >-
                    v2_060000231003b20faec8c7e28811c4d5cc0ded37b0779c48c759a7446a87688c2774e5300c32@finder
                  nickname: 未来可期啊哈
                  headUrl: >-
                    https://wx.qlogo.cn/finderhead/ver_1/D5kOMSrTOprOibFVZ2NOO8AnohFdlDMhoNTZr1C8D9d5K6og92mcc3lxDEFcQldBibqjzIx2iavenQO0TMzhjmrUibmn3iaoaLYtNiaGFWjZgCd5t92shsicTvcyiaIjFjRtwVgy/0
                  signature: 理智，清醒，知进退。
                  followFlag: 1
                  authInfo: {}
                  coverImgUrl: ''
                  spamStatus: 0
                  extFlag: 262152
                  extInfo:
                    sex: 1
                  liveStatus: 2
                  liveCoverImgUrl: ''
                  liveInfo:
                    anchorStatusFlag: 2048
                    switchFlag: 53727
                    lotterySetting:
                      settingFlag: 0
                      attendType: 4
                  status: 0
          headers: {}
          x-apifox-name: 成功
      security: []
      x-apifox-folder: 基础API/视频号模块
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3475559/apis/api-144600734-run
components:
  schemas: {}
  securitySchemes: {}
servers:
  - url: http://218.78.116.24:10883
    description: 测试环境
security: []

```

# 搜索并关注

> 和[发布视频接口](http://doc.geweapi.com/endpoint-144557553)实现的功能一样，此接口建议多个号批量发布时使用，某个号调用1次[上传CDN视频](http://doc.geweapi.com/endpoint-144561904)，其余号直接调用[CDN发布](http://doc.geweapi.com/endpoint-144563194)，无需重复上传。

## OpenAPI

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /gewe/v2/api/finder/searchFollow:
    post:
      summary: 搜索并关注
      deprecated: false
      description: >-
        和[发布视频接口](http://doc.geweapi.com/endpoint-144557553)实现的功能一样，此接口建议多个号批量发布时使用，某个号调用1次[上传CDN视频](http://doc.geweapi.com/endpoint-144561904)，其余号直接调用[CDN发布](http://doc.geweapi.com/endpoint-144563194)，无需重复上传。
      tags:
        - 基础API/视频号模块
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
                myUserName:
                  type: string
                myRoleType:
                  type: integer
                toUserName:
                  type: string
                keyword:
                  type: string
              required:
                - appId
                - myUserName
                - myRoleType
                - toUserName
                - keyword
              x-apifox-orders:
                - appId
                - myUserName
                - myRoleType
                - toUserName
                - keyword
            example:
              appId: '{{appid}}'
              myUserName: '{{userName}}'
              myRoleType: 3
              toUserName: v2_06**23c0fe3c@finder
              keyword: 乡村彩妹儿
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
      x-apifox-folder: 基础API/视频号模块
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3475559/apis/api-282523896-run
components:
  schemas: {}
  securitySchemes: {}
servers:
  - url: http://218.78.116.24:10883
    description: 测试环境
security: []

```

# 扫码浏览

## OpenAPI

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /gewe/v2/api/finder/scanBrowse:
    post:
      summary: 扫码浏览
      deprecated: false
      description: ''
      tags:
        - 基础API/视频号模块
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
                myUserName:
                  type: string
                  description: 自己的username
                myRoleType:
                  type: integer
                  description: 自己的roletype
                qrContent:
                  type: string
                  description: 获取方式：官方视频号助手->内容管理->视频->复制视频链接
                objectId:
                  type: integer
                  description: 视频号的objectId
              required:
                - appId
                - myUserName
                - myRoleType
                - qrContent
                - objectId
              x-apifox-orders:
                - appId
                - myUserName
                - myRoleType
                - qrContent
                - objectId
            example:
              appId: '{{appid}}'
              proxyIp: ''
              myUserName: >-
                v2_060000231003b20faec8c7e28811c4d5cc0ded37b0779c48c759a7446a87688c2774e5300c32@finder
              myRoleType: 3
              qrContent: https://weixin.qq.com/sph/ArJBdPlIM
              objectId: 14195037502970006000
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
              example:
                ret: 200
                msg: 操作成功
          headers: {}
          x-apifox-name: 成功
      security: []
      x-apifox-folder: 基础API/视频号模块
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3475559/apis/api-144601719-run
components:
  schemas: {}
  securitySchemes: {}
servers:
  - url: http://218.78.116.24:10883
    description: 测试环境
security: []

```

# 扫码评论

## OpenAPI

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /gewe/v2/api/finder/scanComment:
    post:
      summary: 扫码评论
      deprecated: false
      description: ''
      tags:
        - 基础API/视频号模块
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
                myUserName:
                  type: string
                  description: 自己的username
                myRoleType:
                  type: integer
                  description: 自己的roletype
                qrContent:
                  type: string
                  description: 获取方式：官方视频号助手->内容管理->视频->复制视频链接
                objectId:
                  type: integer
                  description: 视频号的objectId（获取用户主页返回的视频id）
                commentContent:
                  type: string
                  description: 评论内容
                replyUsername:
                  type: string
                  description: 回复的username
                refCommentId:
                  type: integer
                  description: 回复评论时传
                rootCommentId:
                  type: integer
                  description: 回复评论时传
              required:
                - appId
                - myUserName
                - myRoleType
                - qrContent
                - objectId
                - commentContent
              x-apifox-orders:
                - appId
                - myUserName
                - myRoleType
                - qrContent
                - objectId
                - commentContent
                - replyUsername
                - refCommentId
                - rootCommentId
            example:
              appId: '{{appid}}'
              proxyIp: ''
              myUserName: >-
                v2_060000231003b20faec8c7e28811c4d5cc0ded37b0779c48c759a7446a87688c2774e5300c32@finder
              myRoleType: 3
              qrContent: https://weixin.qq.com/sph/ArJBdPlIM
              objectId: 14195037502970006000
              commentContent: hhh
              replyUsername: ''
              refCommentId: 0
              rootCommentId: 0
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
                      commentId:
                        type: integer
                        description: 评论ID
                      clientid:
                        type: string
                    required:
                      - commentId
                      - clientid
                    x-apifox-orders:
                      - commentId
                      - clientid
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
                  commentId: 14311728323297282000
                  clientid: '988946786'
          headers: {}
          x-apifox-name: 成功
      security: []
      x-apifox-folder: 基础API/视频号模块
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3475559/apis/api-144601935-run
components:
  schemas: {}
  securitySchemes: {}
servers:
  - url: http://218.78.116.24:10883
    description: 测试环境
security: []

```

# 扫码点赞

## OpenAPI

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /gewe/v2/api/finder/scanFav:
    post:
      summary: 扫码点赞
      deprecated: false
      description: ''
      tags:
        - 基础API/视频号模块
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
                myUserName:
                  type: string
                  description: 自己的username
                myRoleType:
                  type: integer
                  description: 自己的roletype
                qrContent:
                  type: string
                  description: 获取方式：官方视频号助手->内容管理->视频->复制视频链接
                objectId:
                  type: integer
                  description: 视频号的objectId（获取用户主页返回的视频id）
              required:
                - appId
                - myUserName
                - myRoleType
                - qrContent
                - objectId
              x-apifox-orders:
                - appId
                - myUserName
                - myRoleType
                - qrContent
                - objectId
            example:
              appId: '{{appid}}'
              proxyIp: ''
              myUserName: >-
                v2_060000231003b20faec8c7e28811c4d5cc0ded37b0779c48c759a7446a87688c2774e5300c32@finder
              myRoleType: 3
              qrContent: https://weixin.qq.com/sph/ArJBdPlIM
              objectId: 14195037502970006000
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
              example:
                ret: 200
                msg: 操作成功
          headers: {}
          x-apifox-name: 成功
      security: []
      x-apifox-folder: 基础API/视频号模块
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3475559/apis/api-144601495-run
components:
  schemas: {}
  securitySchemes: {}
servers:
  - url: http://218.78.116.24:10883
    description: 测试环境
security: []

```

# 扫码点小红心

## OpenAPI

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /gewe/v2/api/finder/scanLike:
    post:
      summary: 扫码点小红心
      deprecated: false
      description: ''
      tags:
        - 基础API/视频号模块
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
                myUserName:
                  type: string
                  description: 自己的username
                myRoleType:
                  type: integer
                  description: 自己的roletype
                qrContent:
                  type: string
                  description: 获取方式：官方视频号助手->内容管理->视频->复制视频链接
                objectId:
                  type: integer
                  description: 视频号的objectId（获取用户主页返回的视频id）
              required:
                - appId
                - myUserName
                - myRoleType
                - qrContent
                - objectId
              x-apifox-orders:
                - appId
                - myUserName
                - myRoleType
                - qrContent
                - objectId
            example:
              appId: '{{appid}}'
              proxyIp: ''
              myUserName: >-
                v2_060000231003b20faec8c7e28811c4d5cc0ded37b0779c48c759a7446a87688c2774e5300c32@finder
              myRoleType: 3
              qrContent: https://weixin.qq.com/sph/ArJBdPlIM
              objectId: 0
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
              example:
                ret: 200
                msg: 操作成功
          headers: {}
          x-apifox-name: 成功
      security: []
      x-apifox-folder: 基础API/视频号模块
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3475559/apis/api-144600850-run
components:
  schemas: {}
  securitySchemes: {}
servers:
  - url: http://218.78.116.24:10883
    description: 测试环境
security: []

```

# 延迟点赞、小红心

> 和[发布视频接口](http://doc.geweapi.com/endpoint-144557553)实现的功能一样，此接口建议多个号批量发布时使用，某个号调用1次[上传CDN视频](http://doc.geweapi.com/endpoint-144561904)，其余号直接调用[CDN发布](http://doc.geweapi.com/endpoint-144563194)，无需重复上传。

## OpenAPI

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /gewe/v2/api/finder/finderOpt:
    post:
      summary: 延迟点赞、小红心
      deprecated: false
      description: >-
        和[发布视频接口](http://doc.geweapi.com/endpoint-144557553)实现的功能一样，此接口建议多个号批量发布时使用，某个号调用1次[上传CDN视频](http://doc.geweapi.com/endpoint-144561904)，其余号直接调用[CDN发布](http://doc.geweapi.com/endpoint-144563194)，无需重复上传。
      tags:
        - 基础API/视频号模块
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
                myUserName:
                  type: string
                myRoleType:
                  type: integer
                toUserName:
                  type: string
                opType:
                  description: 1点赞 3小红心
                  type: integer
                id:
                  type: string
                remain:
                  type: integer
              required:
                - appId
                - myUserName
                - myRoleType
                - toUserName
                - opType
                - id
                - remain
              x-apifox-orders:
                - appId
                - myUserName
                - myRoleType
                - toUserName
                - opType
                - id
                - remain
            example: |-
              {
                  "appId": "{{appid}}",
                  "myUserName": "{{userName}}",
                  "myRoleType": 3,
                  "toUserName": "v2_060000**7f806638a8@finder",
                  "opType": 1,//1点赞 3小红心
                  "id": "14618**2729205",
                  "remain": 3
              }
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
      x-apifox-folder: 基础API/视频号模块
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3475559/apis/api-282525999-run
components:
  schemas: {}
  securitySchemes: {}
servers:
  - url: http://218.78.116.24:10883
    description: 测试环境
security: []

```

# 扫码登录视频号助手

## OpenAPI

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /gewe/v2/api/finder/scanLoginChannels:
    post:
      summary: 扫码登录视频号助手
      deprecated: false
      description: ''
      tags:
        - 基础API/视频号模块
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
                qrContent:
                  type: string
                  description: 视频号助手官方二维码解析出来的内容
              required:
                - appId
                - qrContent
              x-apifox-orders:
                - appId
                - qrContent
            example:
              appId: '{{appid}}'
              proxyIp: ''
              qrContent: >-
                https://channels.weixin.qq.com/mobile/confirm_login.html?token=AQAAAAU6Z4vTAheiPSH4Ew
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
                      sessionId:
                        type: string
                        description: sessionid
                      finderList:
                        type: array
                        items:
                          type: object
                          properties:
                            finderUsername:
                              type: string
                              description: 视频号的username
                            nickname:
                              type: string
                              description: 昵称
                            headImgUrl:
                              type: string
                              description: 头像
                            coverImgUrl:
                              type: string
                            spamFlag:
                              type: integer
                            acctType:
                              type: integer
                            authIconType:
                              type: integer
                            ownerWxUin:
                              type: integer
                            adminNickname:
                              type: string
                            categoryFlag:
                              type: string
                            uniqId:
                              type: string
                            isMasterFinder:
                              type: boolean
                          x-apifox-orders:
                            - finderUsername
                            - nickname
                            - headImgUrl
                            - coverImgUrl
                            - spamFlag
                            - acctType
                            - authIconType
                            - ownerWxUin
                            - adminNickname
                            - categoryFlag
                            - uniqId
                            - isMasterFinder
                      acctStatus:
                        type: integer
                    required:
                      - finderList
                      - sessionId
                      - acctStatus
                    x-apifox-orders:
                      - sessionId
                      - finderList
                      - acctStatus
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
                  finderList:
                    - finderUsername: >-
                        v2_060000231003b20faec8c7e28811c4d5cc0ded37b0779c48c759a7446a87688c2774e5300c32@finder
                      nickname: 未来可期啊哈
                      headImgUrl: >-
                        https://wx.qlogo.cn/finderhead/AbruuZ3ILCkWiallQicn8kbXiafrvbTc6uMOYyC7WiaOzmle9GcMavFI3nSdMsAc916JoG9DRWAEHew/0
                      coverImgUrl: ''
                      spamFlag: 0
                      acctType: 1
                      authIconType: 0
                      ownerWxUin: 4077276085
                      adminNickname: G
                      categoryFlag: '0'
                      uniqId: sphCDn31wJCgtzi
                      isMasterFinder: true
                  sessionId: >-
                    BgAAS3uHm+iGloBRhbJ8+tn7PEGx/DcCOXiC4hSt1OsQBeUWNPoZkN4RMA/EdY3se+v6ZQLdjxJimUko/Y1rjgmm/chqg36qojh2
                  acctStatus: 1
          headers: {}
          x-apifox-name: 成功
      security: []
      x-apifox-folder: 基础API/视频号模块
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3475559/apis/api-144556473-run
components:
  schemas: {}
  securitySchemes: {}
servers:
  - url: http://218.78.116.24:10883
    description: 测试环境
security: []

```

# 扫码获取视频详情

## OpenAPI

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /gewe/v2/api/finder/scanQrCode:
    post:
      summary: 扫码获取视频详情
      deprecated: false
      description: ''
      tags:
        - 基础API/视频号模块
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
                myUserName:
                  type: string
                  description: 自己的username
                myRoleType:
                  type: integer
                  description: 自己的roletype
                qrContent:
                  type: string
                  description: 获取方式：官方视频号助手->内容管理->视频->复制视频链接
              required:
                - appId
                - myUserName
                - myRoleType
                - qrContent
              x-apifox-orders:
                - appId
                - myUserName
                - myRoleType
                - qrContent
            example:
              appId: '{{appid}}'
              proxyIp: ''
              myUserName: >-
                v2_060000231003b20faec8c7e28811c4d5cc0ded37b0779c48c759a7446a87688c2774e5300c32@finder
              myRoleType: 3
              qrContent: https://weixin.qq.com/sph/Apv77JRt5
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
                      object:
                        type: object
                        properties:
                          id:
                            type: integer
                            description: 作品ID
                          nickname:
                            type: string
                            description: 昵称
                          username:
                            type: string
                            description: 视频作者的username
                          objectDesc:
                            type: object
                            properties:
                              description:
                                type: string
                                description: 作品描述
                              media:
                                type: array
                                items:
                                  type: object
                                  properties:
                                    Url:
                                      type: string
                                      description: 视频链接
                                    ThumbUrl:
                                      type: string
                                      description: 封面图链接
                                    MediaType:
                                      type: integer
                                    VideoPlayLen:
                                      type: integer
                                    Width:
                                      type: integer
                                      description: 宽度
                                    Height:
                                      type: integer
                                      description: 高度
                                    Md5Sum:
                                      type: string
                                      description: 文件md5
                                    FileSize:
                                      type: integer
                                      description: 文件大小
                                    Bitrate:
                                      type: integer
                                      description: 码率
                                    coverUrl:
                                      type: string
                                    decodeKey:
                                      type: string
                                    urlToken:
                                      type: string
                                    thumbUrlToken:
                                      type: string
                                    codecInfo:
                                      type: object
                                      properties:
                                        thumbScore:
                                          type: integer
                                        hdimgScore:
                                          type: integer
                                      required:
                                        - thumbScore
                                        - hdimgScore
                                      x-apifox-orders:
                                        - thumbScore
                                        - hdimgScore
                                    fullThumbUrl:
                                      type: string
                                    fullThumbUrlToken:
                                      type: string
                                    fullCoverUrl:
                                      type: string
                                    liveCoverImgs:
                                      type: array
                                      items:
                                        type: object
                                        properties:
                                          ThumbUrl:
                                            type: string
                                          FileSize:
                                            type: integer
                                          Width:
                                            type: integer
                                          Height:
                                            type: integer
                                          Bitrate:
                                            type: integer
                                        required:
                                          - ThumbUrl
                                          - FileSize
                                          - Width
                                          - Height
                                          - Bitrate
                                        x-apifox-orders:
                                          - ThumbUrl
                                          - FileSize
                                          - Width
                                          - Height
                                          - Bitrate
                                    cardShowStyle:
                                      type: integer
                                    dynamicRangeType:
                                      type: integer
                                    videoType:
                                      type: integer
                                  required:
                                    - Url
                                    - ThumbUrl
                                    - MediaType
                                    - VideoPlayLen
                                    - Width
                                    - Height
                                    - Md5Sum
                                    - FileSize
                                    - Bitrate
                                    - coverUrl
                                    - decodeKey
                                    - urlToken
                                    - thumbUrlToken
                                    - codecInfo
                                    - fullThumbUrl
                                    - fullThumbUrlToken
                                    - fullCoverUrl
                                    - liveCoverImgs
                                    - cardShowStyle
                                    - dynamicRangeType
                                    - videoType
                                  x-apifox-orders:
                                    - Url
                                    - ThumbUrl
                                    - MediaType
                                    - VideoPlayLen
                                    - Width
                                    - Height
                                    - Md5Sum
                                    - FileSize
                                    - Bitrate
                                    - coverUrl
                                    - decodeKey
                                    - urlToken
                                    - thumbUrlToken
                                    - codecInfo
                                    - fullThumbUrl
                                    - fullThumbUrlToken
                                    - fullCoverUrl
                                    - liveCoverImgs
                                    - cardShowStyle
                                    - dynamicRangeType
                                    - videoType
                              mediaType:
                                type: integer
                              location:
                                type: object
                                properties: {}
                                x-apifox-orders: []
                              extReading:
                                type: object
                                properties: {}
                                x-apifox-orders: []
                              topic:
                                type: object
                                properties:
                                  finderTopicInfo:
                                    type: string
                                required:
                                  - finderTopicInfo
                                x-apifox-orders:
                                  - finderTopicInfo
                              followPostInfo:
                                type: object
                                properties:
                                  musicInfo:
                                    type: object
                                    properties:
                                      docId:
                                        type: string
                                      albumThumbUrl:
                                        type: string
                                        description: 缩率图
                                      name:
                                        type: string
                                        description: 音乐名
                                      artist:
                                        type: string
                                        description: 作者名
                                      albumName:
                                        type: string
                                      mediaStreamingUrl:
                                        type: string
                                        description: 音乐播放链接
                                      miniappInfo:
                                        type: string
                                      webUrl:
                                        type: string
                                      floatThumbUrl:
                                        type: string
                                      chorusBegin:
                                        type: integer
                                      docType:
                                        type: integer
                                      songId:
                                        type: string
                                    required:
                                      - docId
                                      - albumThumbUrl
                                      - name
                                      - artist
                                      - albumName
                                      - mediaStreamingUrl
                                      - miniappInfo
                                      - webUrl
                                      - floatThumbUrl
                                      - chorusBegin
                                      - docType
                                      - songId
                                    x-apifox-orders:
                                      - docId
                                      - albumThumbUrl
                                      - name
                                      - artist
                                      - albumName
                                      - mediaStreamingUrl
                                      - miniappInfo
                                      - webUrl
                                      - floatThumbUrl
                                      - chorusBegin
                                      - docType
                                      - songId
                                    description: 背景音乐信息
                                  groupId:
                                    type: string
                                  hasBgm:
                                    type: integer
                                required:
                                  - musicInfo
                                  - groupId
                                  - hasBgm
                                x-apifox-orders:
                                  - musicInfo
                                  - groupId
                                  - hasBgm
                              fromApp:
                                type: object
                                properties: {}
                                x-apifox-orders: []
                              event:
                                type: object
                                properties: {}
                                x-apifox-orders: []
                              mvInfo:
                                type: object
                                properties: {}
                                x-apifox-orders: []
                              draftObjectId:
                                type: integer
                              clientDraftExtInfo:
                                type: object
                                properties:
                                  lbsFlagType:
                                    type: integer
                                  videoMusicId:
                                    type: string
                                required:
                                  - lbsFlagType
                                  - videoMusicId
                                x-apifox-orders:
                                  - lbsFlagType
                                  - videoMusicId
                              generalReportInfo:
                                type: object
                                properties: {}
                                x-apifox-orders: []
                              posterLocation:
                                type: object
                                properties:
                                  longitude:
                                    type: number
                                    description: 经度
                                  latitude:
                                    type: number
                                    description: 纬度
                                  city:
                                    type: string
                                    description: 城市
                                required:
                                  - longitude
                                  - latitude
                                  - city
                                x-apifox-orders:
                                  - longitude
                                  - latitude
                                  - city
                                description: 作品发布位置
                              shortTitle:
                                type: array
                                items:
                                  type: string
                              originalInfoDesc:
                                type: object
                                properties: {}
                                x-apifox-orders: []
                              finderNewlifeDesc:
                                type: object
                                properties: {}
                                x-apifox-orders: []
                            required:
                              - description
                              - media
                              - mediaType
                              - location
                              - extReading
                              - topic
                              - followPostInfo
                              - fromApp
                              - event
                              - mvInfo
                              - draftObjectId
                              - clientDraftExtInfo
                              - generalReportInfo
                              - posterLocation
                              - shortTitle
                              - originalInfoDesc
                              - finderNewlifeDesc
                            x-apifox-orders:
                              - description
                              - media
                              - mediaType
                              - location
                              - extReading
                              - topic
                              - followPostInfo
                              - fromApp
                              - event
                              - mvInfo
                              - draftObjectId
                              - clientDraftExtInfo
                              - generalReportInfo
                              - posterLocation
                              - shortTitle
                              - originalInfoDesc
                              - finderNewlifeDesc
                          createtime:
                            type: integer
                            description: 发布时间
                          likeFlag:
                            type: integer
                          likeList:
                            type: array
                            items:
                              type: string
                          forwardCount:
                            type: integer
                            description: 转发数
                          contact:
                            type: object
                            properties:
                              username:
                                type: string
                                description: 作者username
                              nickname:
                                type: string
                                description: 昵称
                              headUrl:
                                type: string
                                description: 头像
                              signature:
                                type: string
                                description: 简介
                              authInfo:
                                type: object
                                properties: {}
                                x-apifox-orders: []
                              coverImgUrl:
                                type: string
                              spamStatus:
                                type: integer
                              extFlag:
                                type: integer
                              extInfo:
                                type: object
                                properties:
                                  country:
                                    type: string
                                  province:
                                    type: string
                                  city:
                                    type: string
                                  sex:
                                    type: integer
                                required:
                                  - country
                                  - province
                                  - city
                                  - sex
                                x-apifox-orders:
                                  - country
                                  - province
                                  - city
                                  - sex
                              liveStatus:
                                type: integer
                              liveCoverImgUrl:
                                type: string
                              liveInfo:
                                type: object
                                properties:
                                  anchorStatusFlag:
                                    type: integer
                                  switchFlag:
                                    type: integer
                                  lotterySetting:
                                    type: object
                                    properties:
                                      settingFlag:
                                        type: integer
                                      attendType:
                                        type: integer
                                    required:
                                      - settingFlag
                                      - attendType
                                    x-apifox-orders:
                                      - settingFlag
                                      - attendType
                                required:
                                  - anchorStatusFlag
                                  - switchFlag
                                  - lotterySetting
                                x-apifox-orders:
                                  - anchorStatusFlag
                                  - switchFlag
                                  - lotterySetting
                              status:
                                type: integer
                            required:
                              - username
                              - nickname
                              - headUrl
                              - signature
                              - authInfo
                              - coverImgUrl
                              - spamStatus
                              - extFlag
                              - extInfo
                              - liveStatus
                              - liveCoverImgUrl
                              - liveInfo
                              - status
                            x-apifox-orders:
                              - username
                              - nickname
                              - headUrl
                              - signature
                              - authInfo
                              - coverImgUrl
                              - spamStatus
                              - extFlag
                              - extInfo
                              - liveStatus
                              - liveCoverImgUrl
                              - liveInfo
                              - status
                          likeCount:
                            type: integer
                            description: 点赞数
                          commentCount:
                            type: integer
                            description: 评论数
                          friendLikeCount:
                            type: integer
                            description: 好友点赞数
                          objectNonceId:
                            type: string
                            description: 作品的NonceId
                          objectStatus:
                            type: integer
                          sendShareFavWording:
                            type: string
                          originalFlag:
                            type: integer
                          secondaryShowFlag:
                            type: integer
                          favCount:
                            type: integer
                            description: 点赞数
                          favFlag:
                            type: integer
                          urlValidTime:
                            type: integer
                          forwardStyle:
                            type: integer
                          permissionFlag:
                            type: integer
                          objectType:
                            type: integer
                          followFeedCount:
                            type: integer
                          verifyInfoBuf:
                            type: string
                          wxStatusRefCount:
                            type: integer
                          adFlag:
                            type: integer
                          ringtoneCount:
                            type: integer
                          funcFlag:
                            type: integer
                          ipRegionInfo:
                            type: object
                            properties: {}
                            x-apifox-orders: []
                            description: 地区信息
                        required:
                          - id
                          - nickname
                          - username
                          - objectDesc
                          - createtime
                          - likeFlag
                          - likeList
                          - forwardCount
                          - contact
                          - likeCount
                          - commentCount
                          - friendLikeCount
                          - objectNonceId
                          - objectStatus
                          - sendShareFavWording
                          - originalFlag
                          - secondaryShowFlag
                          - favCount
                          - favFlag
                          - urlValidTime
                          - forwardStyle
                          - permissionFlag
                          - objectType
                          - followFeedCount
                          - verifyInfoBuf
                          - wxStatusRefCount
                          - adFlag
                          - ringtoneCount
                          - funcFlag
                          - ipRegionInfo
                        x-apifox-orders:
                          - id
                          - nickname
                          - username
                          - objectDesc
                          - createtime
                          - likeFlag
                          - likeList
                          - forwardCount
                          - contact
                          - likeCount
                          - commentCount
                          - friendLikeCount
                          - objectNonceId
                          - objectStatus
                          - sendShareFavWording
                          - originalFlag
                          - secondaryShowFlag
                          - favCount
                          - favFlag
                          - urlValidTime
                          - forwardStyle
                          - permissionFlag
                          - objectType
                          - followFeedCount
                          - verifyInfoBuf
                          - wxStatusRefCount
                          - adFlag
                          - ringtoneCount
                          - funcFlag
                          - ipRegionInfo
                      commentCount:
                        type: integer
                        description: 评论数
                      nextCheckObjectStatus:
                        type: integer
                    required:
                      - object
                      - commentCount
                      - nextCheckObjectStatus
                    x-apifox-orders:
                      - object
                      - commentCount
                      - nextCheckObjectStatus
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
                  object:
                    id: 14195037502970006000
                    nickname: 朝夕v
                    username: >-
                      v2_060000231003b20faec8c6e18f10c7d6c903ec3db0776955d3d97c6b329d6aa58693bcdb7ad1@finder
                    objectDesc:
                      description: ''
                      media:
                        - Url: >-
                            http://wxapp.tc.qq.com/251/20304/stodownload?encfilekey=oibeqyX228riaCwo9STVsGLPj9UYCicgttv57KAwaibwgt59R0ZvexpfcXpicuZgK9KrWFnqVIGCmmeEELsRrp14MS0oiaUOguD6XaicBEDD69qqNI2Qaa01Z17Yj56V9olerBgeGv5egDtHJ0&bizid=1023&dotrans=0&hy=SH&idx=1&m=82071545ea946d89af9ea5d6ad0fb576
                          ThumbUrl: >-
                            http://wxapp.tc.qq.com/251/20350/stodownload?encfilekey=oibeqyX228riaCwo9STVsGLPj9UYCicgttv1yP5Z57icAlHCbKIfJMyjc6w0oSrmEBrYXzewfFv2c6gkUHREmCrru0rTbTiaqV0Jvu83Sibd1JTfiaBTdCLQMjO8RQwlCjlC64lA3mHfKN3Jlc&bizid=1023&dotrans=0&hy=SH&idx=1&m=244c5c71db596838df691d372e7c0479&picformat=200
                          MediaType: 2
                          VideoPlayLen: 0
                          Width: 1440
                          Height: 1080
                          Md5Sum: ''
                          FileSize: 297437
                          Bitrate: 0
                          coverUrl: ''
                          decodeKey: '1249495775'
                          urlToken: >-
                            &token=Cvvj5Ix3eew5xyibexEnJ5wHgmp3icrpTu68qEau3f8kYibrgx0C7YJPXzPj5ZmZTrGDaVNPibNqDUluaAnQnYIgnGN0VlYn0RSIYoY8liaMNEe6lb4dvymCx1we4zvlw7Q3M&ctsc=154
                          thumbUrlToken: >-
                            &token=KkOFht0mCXkk40rrFZzjtRLINy4ASRjBT3GpxvY5LeFl3ibt0nm2JyM7A5SefhCxuIaCRLhh8H4aCoMHgTGpVuN23pbEZXtTm3dwjicXpRfmw&ctsc=1-154
                          codecInfo:
                            thumbScore: 12
                            hdimgScore: 45
                          fullThumbUrl: >-
                            http://wxapp.tc.qq.com/251/20350/stodownload?encfilekey=oibeqyX228riaCwo9STVsGLPj9UYCicgttv1yP5Z57icAlHCbKIfJMyjc6w0oSrmEBrYXzewfFv2c6gkUHREmCrru0rTbTiaqV0Jvu83Sibd1JTfiaBTdCLQMjO8RQwlCjlC64lA3mHfKN3Jlc&bizid=1023&dotrans=0&hy=SH&idx=1&m=244c5c71db596838df691d372e7c0479&picformat=200
                          fullThumbUrlToken: >-
                            &token=ic1n0xDG6awibsU5seGwWubKqKDaibhvFe7cNc4g5kibddUiafHicQmQSnP0AqPGO78ibPAstChRj8mVmy0DnNaibpLtmLTzfVCZdIUDyyyPbRwf6yA&ctsc=3-154
                          fullCoverUrl: ''
                          liveCoverImgs:
                            - ThumbUrl: >-
                                http://wxapp.tc.qq.com/251/20350/stodownload?encfilekey=oibeqyX228riaCwo9STVsGLPj9UYCicgttv1yP5Z57icAlHCbKIfJMyjc6w0oSrmEBrYXzewfFv2c6gkUHREmCrru0rTbTiaqV0Jvu83Sibd1JTfiaBTdCLQMjO8RQwlCjlC64lA3mHfKN3Jlc&bizid=1023&dotrans=0&hy=SH&idx=1&m=244c5c71db596838df691d372e7c0479
                              FileSize: 297437
                              Width: 1440
                              Height: 1080
                              Bitrate: 0
                          cardShowStyle: 0
                          dynamicRangeType: 0
                          videoType: 1
                        - Url: >-
                            http://wxapp.tc.qq.com/251/20304/stodownload?encfilekey=oibeqyX228riaCwo9STVsGLPj9UYCicgttvz7tHiay7nNxvJB3XKPvEuUhSdvoK3GckSDiaPJOqZnNaaTZibPYATvktg1qWDEShg5s6g8h79a1udSLNEdrRAPXwgQ4gG3HIyWOyA83V0WqYj0&bizid=1023&dotrans=0&hy=SH&idx=1&m=857ad08a06915c8fd77810d3a0bf6245
                          ThumbUrl: >-
                            http://wxapp.tc.qq.com/251/20350/stodownload?encfilekey=oibeqyX228riaCwo9STVsGLPj9UYCicgttvXia4icia4dYpVyxxmEmnFnndXTLqaibmOPXM2xQ5csekZIDZMOnTahH4bYYL8CsP1Fiadia7hb3y2ianicOjI4wsw8LicoSsOf8DUkGWJNoNc5pDE1FA&bizid=1023&dotrans=0&hy=SH&idx=1&m=e57a332f673663e810b4a7da0bf1e78e&picformat=200
                          MediaType: 2
                          VideoPlayLen: 0
                          Width: 1440
                          Height: 1080
                          Md5Sum: ''
                          FileSize: 326887
                          Bitrate: 0
                          coverUrl: ''
                          decodeKey: '2082100859'
                          urlToken: >-
                            &token=Cvvj5Ix3eew5xyibexEnJ5wHgmp3icrpTuRfgthRqkJo1ILSHgS8CrIYiajXoEsI3Od2cdGFcA5gtpgJFdGlnyXibGOTnA5Mjj57C286SKv1Nx82ibfRw5nWrXD5XDE9v12Wk&ctsc=154
                          thumbUrlToken: >-
                            &token=oA9SZ4icv8IsZenXlysnwuuxdic7Vq0GNRzqzddZpThibnDVkFeibXtr3BM3vIfI15IuYL4XZ4ed3PQZx1CRyJgT7n9gAd1OH2XlUZIRzxcV0ss&ctsc=1-154
                          codecInfo:
                            thumbScore: 12
                            hdimgScore: 45
                          fullThumbUrl: >-
                            http://wxapp.tc.qq.com/251/20350/stodownload?encfilekey=oibeqyX228riaCwo9STVsGLPj9UYCicgttvXia4icia4dYpVyxxmEmnFnndXTLqaibmOPXM2xQ5csekZIDZMOnTahH4bYYL8CsP1Fiadia7hb3y2ianicOjI4wsw8LicoSsOf8DUkGWJNoNc5pDE1FA&bizid=1023&dotrans=0&hy=SH&idx=1&m=e57a332f673663e810b4a7da0bf1e78e&picformat=200
                          fullThumbUrlToken: >-
                            &token=KkOFht0mCXknX5dyibFbricEsibuX5GcA3AOSmtpQrB2rgYdU0FOnE9kTqeDt2PKrc459w86XlluKT2N3byELLzJ7WdyIHibaFHGiaUImGnNamIc&ctsc=3-154
                          fullCoverUrl: ''
                          liveCoverImgs:
                            - ThumbUrl: >-
                                http://wxapp.tc.qq.com/251/20350/stodownload?encfilekey=oibeqyX228riaCwo9STVsGLPj9UYCicgttvXia4icia4dYpVyxxmEmnFnndXTLqaibmOPXM2xQ5csekZIDZMOnTahH4bYYL8CsP1Fiadia7hb3y2ianicOjI4wsw8LicoSsOf8DUkGWJNoNc5pDE1FA&bizid=1023&dotrans=0&hy=SH&idx=1&m=e57a332f673663e810b4a7da0bf1e78e
                              FileSize: 326887
                              Width: 1440
                              Height: 1080
                              Bitrate: 0
                          cardShowStyle: 0
                          dynamicRangeType: 0
                          videoType: 1
                      mediaType: 2
                      location: {}
                      extReading: {}
                      topic:
                        finderTopicInfo: ''
                      followPostInfo:
                        musicInfo:
                          docId: '342066328'
                          albumThumbUrl: >-
                            http://wx.y.gtimg.cn/music/photo_new/T002R500x500M000001kWuR62LAvku_1.jpg
                          name: monsters
                          artist: 苏天伦
                          albumName: ''
                          mediaStreamingUrl: >-
                            https://cover.qpic.cn/206/20302/stodownload?m=b8c992316fbfde34eadf7c76051035ee&filekey=30350201010421301f020200ce040253480410b8c992316fbfde34eadf7c76051035ee02030f703a040d00000004627466730000000131&hy=SH&storeid=323032323039323330353036323130303035363831663139613364666266356336386234306230303030303063653030303034663465&bizid=1023
                          miniappInfo: ''
                          webUrl: ''
                          floatThumbUrl: ''
                          chorusBegin: 0
                          docType: 0
                          songId: ''
                        groupId: '342066328'
                        hasBgm: 1
                      fromApp: {}
                      event: {}
                      mvInfo: {}
                      draftObjectId: 14195067577171968000
                      clientDraftExtInfo:
                        lbsFlagType: 0
                        videoMusicId: '342066328'
                      generalReportInfo: {}
                      posterLocation:
                        longitude: 116.642105
                        latitude: 34.687767
                        city: Xuzhou City
                      shortTitle:
                        - CgA=
                      originalInfoDesc: {}
                      finderNewlifeDesc: {}
                    createtime: 1692180335
                    likeFlag: 0
                    likeList:
                      - >-
                        Cg56aGFuZ2NodWFuMjI4OBIJ5pyd5aSV44CCGgAgvpKAj+jsuf/EASgAOq0BaHR0cHM6Ly93eC5xbG9nby5jbi9tbWhlYWQvdmVyXzEvcEJSaWNkQjNIOTRFcFQ4UFFKM05Ya2xpYzU5WDdYU3NncENKMFRWMXZjcHVxUWxpYjdNSkdHc2JuWk80djBDRjQ4aWNRb0lKUDljbURBcVR4cWJ6MmlidGlhazh6cEl4RTcwMDV3Nmlhb1hiaWJWVEN3UkdFVXV4U2R3bGMwdGNETjZRSVdVSC8xMzJI0JmzrAZgAKoBAA==
                    forwardCount: 1
                    contact:
                      username: >-
                        v2_060000231003b20faec8c6e18f10c7d6c903ec3db0776955d3d97c6b329d6aa58693bcdb7ad1@finder
                      nickname: 朝夕v
                      headUrl: >-
                        https://wx.qlogo.cn/finderhead/ver_1/TDibw5X5xTzpMW9D4GE0YnYUMqPAspF0AibTwhdSFWjyt2tZCMuLVon1PIT6aGulvzvlSZPkDcT06NB6D1eoLicYBKiaBCRDXZJSMEErIGQkQJ8/0
                      signature: 。。。
                      authInfo: {}
                      coverImgUrl: ''
                      spamStatus: 0
                      extFlag: 262156
                      extInfo:
                        country: CN
                        province: Jiangsu
                        city: Xuzhou
                        sex: 2
                      liveStatus: 2
                      liveCoverImgUrl: >-
                        http://wxapp.tc.qq.com/251/20350/stodownload?m=be88b1cb981aa72b3328ccbd22a58e0b&filekey=30340201010420301e020200fb040253480410be88b1cb981aa72b3328ccbd22a58e0b02022814040d00000004627466730000000132&hy=SH&storeid=5649443df0009b8a38399cc84000000fb00004f7e534815c008e0b08dc805c&dotrans=0&bizid=1023
                      liveInfo:
                        anchorStatusFlag: 133248
                        switchFlag: 53727
                        lotterySetting:
                          settingFlag: 0
                          attendType: 4
                      status: 0
                    likeCount: 2
                    commentCount: 5
                    friendLikeCount: 1
                    objectNonceId: '16628169456191691547_0_154_0_0'
                    objectStatus: 0
                    sendShareFavWording: ''
                    originalFlag: 0
                    secondaryShowFlag: 1
                    favCount: 3
                    favFlag: 1
                    urlValidTime: 172800
                    forwardStyle: 0
                    permissionFlag: 2147483648
                    objectType: 0
                    followFeedCount: 17
                    verifyInfoBuf: >-
                      CrADD3QLRKZljCPO5dJ958TJct7WbHzU3lM4r1PJtQpm8vbngWNGW346SKEAwM8tRL25uHNJfTR0co1F4k76AQY1EDg2GyDaz4PGCeyfiSP5uN6xS0sdYGw+ln0TdVVk1/clsefJAGJscIYDcfTms18Dkw4D79zgBGq3luGMY1TGRcjkopsxRvvYKYwB995y3pZXK9DisP1v1jA5ecMrXKuJDI5qIe6O5SYUk+OY5WQtTRZwELDojU/SiuuZ9eZFf2IkWUGL5FHHBxHB7WX3JcoNPyi0zLHyCVdBBkPIebN/w2RwCbwSXLGO+tqg3XYIRD3PC7ALOU1Hum+jwtUczQIqkFTaQZ+q99DdpMv1yYi5D2zCWxni0r/IfjqvuFSoumfErCW5DMDgny4kRZ4lqRhw0d4EDCLEz4Daz3q+vTIAme8yoWk4O8Wvb8FKvZIjjtSYCkXJLl9feh5oPaFsp8mzLrYCcAze+Lwac+0+e0bJRCtLAiw4BAn+CoyBqhfoJHo6QgGsf4j3CEyY9xxZtQDFyLPEW7vCIJF9tM7a5raqZdHCV13OkgvxKa7hhUNELD3P
                    wxStatusRefCount: 0
                    adFlag: 4
                    ringtoneCount: 0
                    funcFlag: 288
                    ipRegionInfo: {}
                  commentCount: 5
                  nextCheckObjectStatus: 30
          headers: {}
          x-apifox-name: 成功
      security: []
      x-apifox-folder: 基础API/视频号模块
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3475559/apis/api-144599568-run
components:
  schemas: {}
  securitySchemes: {}
servers:
  - url: http://218.78.116.24:10883
    description: 测试环境
security: []

```

# 我的视频号二维码

## OpenAPI

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /gewe/v2/api/finder/getQrCode:
    post:
      summary: 我的视频号二维码
      deprecated: false
      description: ''
      tags:
        - 基础API/视频号模块
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
                myUserName:
                  type: string
                  description: 自己的username
                myRoleType:
                  type: integer
                  description: 自己的roletype
              required:
                - appId
                - myUserName
                - myRoleType
              x-apifox-orders:
                - appId
                - myUserName
                - myRoleType
            example:
              appId: '{{appid}}'
              proxyIp: ''
              myUserName: >-
                v2_060000231003b20faec8c7e28811c4d5cc0ded37b0779c48c759a7446a87688c2774e5300c32@finder
              myRoleType: 3
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
                      qrcodeUrl:
                        type: string
                        description: 二维码内包含的信息
                    required:
                      - qrcodeUrl
                    x-apifox-orders:
                      - qrcodeUrl
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
                  qrcodeUrl: https://weixin.qq.com/f/ECgk7AHVuyoGIX6vmDA_jcE
          headers: {}
          x-apifox-name: 成功
      security: []
      x-apifox-folder: 基础API/视频号模块
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3475559/apis/api-144599378-run
components:
  schemas: {}
  securitySchemes: {}
servers:
  - url: http://218.78.116.24:10883
    description: 测试环境
security: []

```

# 上传CDN视频

> 和[发布视频接口](http://doc.geweapi.com/endpoint-144557553)实现的功能一样，此接口建议多个号批量发布时使用，某个号调用1次[上传CDN视频](http://doc.geweapi.com/endpoint-144561904)，其余号直接调用[CDN发布](http://doc.geweapi.com/endpoint-144563194)，无需重复上传。

## OpenAPI

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /gewe/v2/api/finder/uploadFinderVideo:
    post:
      summary: 上传CDN视频
      deprecated: false
      description: >-
        和[发布视频接口](http://doc.geweapi.com/endpoint-144557553)实现的功能一样，此接口建议多个号批量发布时使用，某个号调用1次[上传CDN视频](http://doc.geweapi.com/endpoint-144561904)，其余号直接调用[CDN发布](http://doc.geweapi.com/endpoint-144563194)，无需重复上传。
      tags:
        - 基础API/视频号模块
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
                videoUrl:
                  type: string
                  description: 视频链接地址
                coverImgUrl:
                  type: string
                  description: 封面链接地址
              required:
                - appId
                - videoUrl
                - coverImgUrl
              x-apifox-orders:
                - appId
                - videoUrl
                - coverImgUrl
            example:
              appId: '{{appid}}'
              proxyIp: ''
              videoUrl: >-
                https://cos.ap-shanghai.myqcloud.com/pkg/436fa030-18a45a6e917.mp4
              coverImgUrl: http://dummyimage.com/400x400
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
                        description: 视频文件链接
                      thumbUrl:
                        type: string
                        description: 封面图链接
                      mp4Identify:
                        type: string
                        description: 文件ID
                      fileSize:
                        type: integer
                        description: 文件大小
                      thumbMD5:
                        type: string
                        description: 封面图md5
                      fileKey:
                        type: string
                        description: 文件的key
                    required:
                      - fileUrl
                      - thumbUrl
                      - mp4Identify
                      - fileSize
                      - thumbMD5
                      - fileKey
                    x-apifox-orders:
                      - fileUrl
                      - thumbUrl
                      - mp4Identify
                      - fileSize
                      - thumbMD5
                      - fileKey
                    description: 可通过如下参数调用cdn发布视频接口
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
                      fileUrl: >-
                        http://wxapp.tc.qq.com/251/20302/stodownload?a=1&bizid=1023&dotrans=0&encfilekey=Cvvj5Ix3eexKX1zo1IZZBrQomawdVfSQH1uu2U31EqFrUA5xctbdDlGGkhM5r9b4e7lDdgzBiaffgFRzukh66M2lXMjLCibKxwU0PWibofftsXd4MHJfNM3VHq2dvmoibcEWE363ibcKI0eTQEIjluPstxRwNxUlPI0iamxHoIKIbaxVM&hy=SH&idx=1&m=6e95f9d79588843ac259b780f0cbf20f&token=cztXnd9GyrEsWrS4eJynZnXPAO12gKrhygeBeB1Zic0orX2aeKcU6ZCsuRHVNiaicw7CQ9M5VgFq8Wut9uMm1QQPA&upid=500210
                      thumbUrl: >-
                        http://wxapp.tc.qq.com/251/20350/stodownload?bizid=1023&dotrans=0&encfilekey=okgXGMsUNLEibHKtCw1bRNicxw6C1zsevQuNo2sjfLcsBDAAjgT6M9OY6Z9VcUKoBHpJsck5dZqOdbCEY7gZhWCHqXLHudqbTQQa6KnvfbM2Ria6riace9QG1zPYAcKc12vS4EicdspqvoxNYs8zKX8EfERXEoEcLdwLZ&hy=SH&idx=1&m=704de7ebbc107a51a4f0986253a6d3b6&token=cztXnd9GyrEsWrS4eJynZhicYicwhU5cChkbUOWNwn6llc25ba051o3j5lhJUGZgv4nzSxYfuDf7q3Xiat145wgtQ
                      mp4Identify: ed39cc64d1dbe68dbc4e43127f2bbd37
                      fileSize: 1315979
                      thumbMD5: 704de7ebbc107a51a4f0986253a6d3b6
                      fileKey: '-finder_upload_7212269489_wxid_0xsqb3o0tsvz22'
                '2':
                  summary: 异常示例
                  value:
                    ret: 500
                    msg: 发布视频失败
                    data:
                      code: '-4013'
                      msg: null
          headers: {}
          x-apifox-name: 成功
        '500':
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
                      code:
                        type: string
                      msg:
                        type: 'null'
                    required:
                      - code
                      - msg
                required:
                  - ret
                  - msg
                  - data
          headers: {}
          x-apifox-name: 服务器错误
      security: []
      x-apifox-folder: 基础API/视频号模块
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3475559/apis/api-144561904-run
components:
  schemas: {}
  securitySchemes: {}
servers:
  - url: http://218.78.116.24:10883
    description: 测试环境
security: []

```

# 发布CDN视频

> 和[发布视频接口](http://doc.geweapi.com/endpoint-144557553)实现的功能一样，此接口建议多个号批量发布时使用，某个号调用1次[上传CDN视频](http://doc.geweapi.com/endpoint-144561904)，其余号直接调用[CDN发布](http://doc.geweapi.com/endpoint-144563194)，无需重复上传。

## OpenAPI

```yaml
openapi: 3.0.1
info:
  title: ''
  description: ''
  version: 1.0.0
paths:
  /gewe/v2/api/finder/publishFinderCdn:
    post:
      summary: 发布CDN视频
      deprecated: false
      description: >-
        和[发布视频接口](http://doc.geweapi.com/endpoint-144557553)实现的功能一样，此接口建议多个号批量发布时使用，某个号调用1次[上传CDN视频](http://doc.geweapi.com/endpoint-144561904)，其余号直接调用[CDN发布](http://doc.geweapi.com/endpoint-144563194)，无需重复上传。
      tags:
        - 基础API/视频号模块
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
                topic:
                  type: array
                  items:
                    type: string
                  description: 话题
                myUserName:
                  type: string
                  description: 自己的username
                myRoleType:
                  type: integer
                  description: 自己的roletype
                description:
                  type: string
                  description: 视频号描述
                videoCdn:
                  type: object
                  properties:
                    fileUrl:
                      type: string
                    thumbUrl:
                      type: string
                    mp4Identify:
                      type: string
                    fileSize:
                      type: integer
                    thumbMD5:
                      type: string
                    fileKey:
                      type: string
                  required:
                    - fileUrl
                    - thumbUrl
                    - mp4Identify
                    - fileSize
                    - thumbMD5
                    - fileKey
                  x-apifox-orders:
                    - fileUrl
                    - thumbUrl
                    - mp4Identify
                    - fileSize
                    - thumbMD5
                    - fileKey
                  description: 视频的cdn信息，通过/uploadFinderVideo接口获取
              required:
                - appId
                - topic
                - myUserName
                - myRoleType
                - description
                - videoCdn
              x-apifox-orders:
                - appId
                - topic
                - myUserName
                - myRoleType
                - description
                - videoCdn
            example:
              appId: '{{appid}}'
              proxyIp: ''
              topic:
                - '#hh'
                - '#哈哈'
              myUserName: >-
                v2_060000231003b20faec8c7e28811c4d5cc0ded37b0779c48c759a7446a87688c2774e5300c32@finder
              myRoleType: 3
              description: hhh
              videoCdn:
                fileUrl: >-
                  http://wxapp.tc.qq.com/251/20302/stodownload?a=1&bizid=1023&dotrans=0&encfilekey=Cvvj5Ix3eexKX1zo1IZZBrQomawdVfSQH1uu2U31EqFrUA5xctbdDlGGkhM5r9b4e7lDdgzBiaffgFRzukh66M2lXMjLCibKxwU0PWibofftsXd4MHJfNM3VHq2dvmoibcEWE363ibcKI0eTQEIjluPstxRwNxUlPI0iamxHoIKIbaxVM&hy=SH&idx=1&m=6e95f9d79588843ac259b780f0cbf20f&token=cztXnd9GyrEsWrS4eJynZnXPAO12gKrhygeBeB1Zic0orX2aeKcU6ZCsuRHVNiaicw7CQ9M5VgFq8Wut9uMm1QQPA&upid=500210
                thumbUrl: >-
                  http://wxapp.tc.qq.com/251/20350/stodownload?bizid=1023&dotrans=0&encfilekey=okgXGMsUNLEibHKtCw1bRNicxw6C1zsevQuNo2sjfLcsBDAAjgT6M9OY6Z9VcUKoBHpJsck5dZqOdbCEY7gZhWCHqXLHudqbTQQa6KnvfbM2Ria6riace9QG1zPYAcKc12vS4EicdspqvoxNYs8zKX8EfERXEoEcLdwLZ&hy=SH&idx=1&m=704de7ebbc107a51a4f0986253a6d3b6&token=cztXnd9GyrEsWrS4eJynZhicYicwhU5cChkbUOWNwn6llc25ba051o3j5lhJUGZgv4nzSxYfuDf7q3Xiat145wgtQ
                mp4Identify: ed39cc64d1dbe68dbc4e43127f2bbd37
                fileSize: 1315979
                thumbMD5: 704de7ebbc107a51a4f0986253a6d3b6
                fileKey: '-finder_upload_7212269489_wxid_0xsqb3o0tsvz22'
      responses:
        '500':
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
                      code:
                        type: string
                      msg:
                        type: 'null'
                        description: 作品ID
                    required:
                      - code
                      - msg
                    x-apifox-orders:
                      - code
                      - msg
                required:
                  - ret
                  - msg
                  - data
                x-apifox-orders:
                  - ret
                  - msg
                  - data
              example:
                ret: 500
                msg: 发布cdn视频失败
                data:
                  code: '-4013'
                  msg: null
          headers: {}
          x-apifox-name: 服务器错误
      security: []
      x-apifox-folder: 基础API/视频号模块
      x-apifox-status: released
      x-run-in-apifox: https://app.apifox.com/web/project/3475559/apis/api-144563194-run
components:
  schemas: {}
  securitySchemes: {}
servers:
  - url: http://218.78.116.24:10883
    description: 测试环境
security: []

```