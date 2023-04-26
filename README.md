# brief description
- This is an application built upon python3 kivy framework.
- This application can run on manny OS

# dependencies
Python 环境 3.10.7


第三方库：安装方法见 <a href="./depen.sh">depen.sh</a> 或 
- chardet
- pillow (PIL)
- promise
- pycrypto (Crypto)
- kivy
- requests
- validator
- statemachine_decorator

Other python builtins dependencies:
- csv
- datetime
- json
- pathlib
- shelve
- time


# struct
| file/directory        | description                                        | detail                                         |
|-----------------------|----------------------------------------------------|------------------------------------------------|
| `main.py`             | 应用程序入口脚本                                           |                                                |
| `clear_data.py`       | 运行此脚本会清除所有用户数据                                     |                                                |
| `countlines.py`       | 运行此脚本会输出项目中所有python和kv文件行数以及它们行数之和                 |                                                |
| `database/users.db`   | 储存所有用户信息的数据库文件                                     | <a href="#users.db detail">users.db detail</a> |
| `database/logs.csv`   | 记录用户操作的csv表格                                       | <a href="#logs.csv detail">logs.csv detail</a> | 
| `database/fileroot`   | 所有用户的根目录                                           | <a href="#fileroot detail">fileroot detail</a> |
| `resource`            | 存放所有程序用到的静态资源                                      ||
| `src`                 | 此表下面的文件或目录皆在`src`目录之下                              |
| `config.py`           | 运行一些配置脚本                                           |
| `sysapp.py`           | 定义主 `App` 类                                        |
| `sysscreens.py`       | 定义应用程序多界面管理器 `SysScreens`类                         |                                                |
| `sys.kv`              | kivy应用程序入口kv文件，用于导入其他所有组件的kv文件                     |                                                |
| `sysscreens.kv`       | 定义 `SysScreens` 界面管理器的结构                           |                                                |
| `components`          | 此目录之下编写了应用程序的大部分组件 python 定义以及 kv 描述，其目录结构与组件数结构相似 |                                                |
| `entities/user.py`    | 定义 `User` 类和 `Users` 类                             |
| `entities/fileobj.py` | 定义 `FileObj` 等继承自`pathlib.Path`的子类，用于管理文件IO处理      |                                                |


## <div id="users.db detail">users.db detail</div>

此文件在用户注册时由 shelve 编写，其结构如下

```py
{
    '210723194905264810': {
        'name': '金永阁',
        'password': '123456',
        'department': '管理部', # "研发部" | "推广部" | "工程部" | "管理部"
        'type': '超级管理员',       # 用户 | 管理员 | 超级管理员
        'state': 'plain',       # 'frozen' 代表账户被冻结, 'plain' 表示正常
    }
}
```

## <div id="logs.csv detail">logs.csv detail<div>
本文件每行记录了用户对文件的操作
第一行是 header，定义了一个操作记录的字段，含义如下:
* time: 操作时间，精确到秒
* operator: 操作者，总为当前登录的用户
* operate: 操作类型，有"查看"、"发送"、"加密"、"解密"、"删除"、"打印"这六个值
* filename: 操作的文件名，不包括其路径
* relate: 与之相关的用户姓名
  * 若操作类型为"查看"，则relate值为文件的作者，可能为文件的发送者（当文件为被发送给用户的），也可能为用户自身（当文件为用户自身上传）
  * 若操作类型为"发送"，则relate值为接收文件的用户
  * 若操作类型为"加密"或"解密'，则relate值都为用户自身
  * 若操作类型为"删除"，则relate值为文件的作者，可能为用户也可能为文件发送者
  * 若操作类型为"打印"，则relate值为文件的作者，可能为用户，也可能为文件发送者，也可能为其他把文件发布到广场上的用户
## <div id="fileroot">fileroot detail</div>

它的目录结构如下所示

- database
  - users.db (用户信息数据库)
  - logs.csv (用户操作信息记录)
  - fileroot (用户根目录，用户所有文件——密钥、上传的文件、接收的文件，都在此存储)
    - 210723194905264810 (金永阁 用户根目录)
      - keys
        - .pub    (注册时创建，RSA公钥)
        - .pri    (注册时创建，RSA私钥)
        - .deskey (DES 密钥，用于加密文件)
      - file
          - f1.txt (公开文件——只能以.txt为后缀名)
          - f2.txt (公开文件)
          - f3.e   (私有文件——以.e为后缀名)
      - recieve (金永阁 用户接收文件根目录)
        - 210723195108294827 (来自 徐宝华 用户发送的文件根目录)
          - f.e   (f.txt 的密文)
          - f.sig (f.e 通过 MD5 和 徐宝华用户的 私钥进行签名产生的文件)
    - 210723195108294827 （徐宝华 用户根目录）
      - keys
        - .pub
        - .pri
        - .deskey
      - file
        - f.txt (此文件被发送给 金永阁 用户)
      - recieve

# 业务逻辑

<pre>
启动程序
  --> 登录账号 --|
  --> 注册账号 --->进入工作页面 --> 查看个人信息
                            --> 查看文件信息 --> 查看"我"上传的文件 --> 发送文件
                                                               --> 加解密文件
                                                               --> 删除文件
                                                              --> 打印输出为PNG图片
                                          --> 查看接收的文件     --> 删除文件
                                                              --> 打印文件为PNG图片
                                          --> 查看发送给他人的文件--> 打印文件为PNG图片
                                          --> 查看所有人公开的文件--> 打印文件为PNG图片
                            --> 查看用户信息 --> 仅查看
                                           --> 冻结\解冻用户（用户是否可以登入）
  --> 退出程序
</pre>
# 补充说明
打印文件时，添加的水印内容为文件作者的姓名。可以启用或关闭水印

正常流程注册账号需要调用***阿里云身份验证接口***，此接口***使用次数有限***，总共两百次，已经使用了*x*次。
可以修改一个变量避免调用此接口，但是还是会用***正则表达式***来验证输入的身份证号和姓名***是否合法***.修改的变量见
./src/components/loginscreen/loginscreen.py 第***183***行的代码

上传的文件只允许为***.txt***后缀名，将被视为纯文本，编码将被自动推断加密的文件后缀为 ***.e***，***接收***的文件将为.e后缀名，且附带一个.sig的签名文件，若签名验证不通过，或原.e文件损坏导致解密出错，都会弹窗提醒用户并显示"未知内容"作为文件内容

开发过程中可能修改了第三方库的某些源代码，如果安装完了依赖还是不能跑，显示报错，联系技术。

若要恢复到初始版本，只需运行 resume.sh （或windows下 resume.bat）即可。