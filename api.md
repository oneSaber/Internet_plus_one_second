1. 注册 '/register', method = 'POST'
请求参数 
{
    参数名；参数类型；参数说明
    email;string;用户的注册email
    username;password;用户的注册昵称， '^[A-Za-z][A-Za-z0-9_.]*$', 0,
                'Usernames must have only letters, numbers, dots or '
                'underscores'
    password;string;用户注册的密码，注册时前端将password hash 化后在发送给后端
}
返回参数
{
    返回string;情况说明
    'successful';注册成功
    'email used';邮箱以注册
    'db error';数据库出错，重新注册
}

2. 登陆 '/login',method=POST
请求参数
{
    参数名;参数类型；参数说明
    email;string;用户用于登陆的email
    password;password;用户密码
    remember_me;bool;记住我
}
返回参数
{
    返回string;情况说明
    'no user';用户未注册
    'password wrong';密码错误
    'login  successful'登陆成功
}

3. 退出登陆 '/logout' method = 'GET'
请求参数：无
返回参数
{
    ‘login successflu';退出成功
}

4. 上传图片 '/upload_file' methods='POST'
请求参数
{
    参数名；参数类型；参数说明
    photo;files;用户上传的图片
    picture_name;string;用户为图片的命名
}
返回参数
{
    返回string;情况说明
    'upload successful';上传成功
    ‘upload fail';上传失败
}

5. 点赞/取消赞 '/star' methods=['POST','DELETE']
请求参数
{
    参数名;参数类型;参数说明
    id;int;图片id
    mothod:POST;点赞图片
    method:DELETE;取消对图片的点赞
}
返回参数
{
    返回string;情况说明
    'successful',操作成功
    'fail'，操作失败
}

6. 点赞/取消赞 '/collect' methods=['POST','DELETE']
请求参数
{
    参数名;参数类型;参数说明
    id;int;图片id
    mothod:POST;收藏图片
    method:DELETE;取消对图片的收藏
}
返回参数
{
    返回string;情况说明
    'successful',操作成功
    'fail'，操作失败
}

7. 删除图片，仅管理员和图片作者本人拥有权限 '/delete-pic',method= 'POST'
请求参数
{
    参数名；参数类型；参数说明
    id;int;图片id
}
返回参数
{
    返回string;情况说明
    'successful',操作成功
    'fail'，操作失败
}
