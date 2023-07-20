-- 初始化SQL
-- 创建admin超级管理员账户, 密码为123456
insert into users(username, password, status) values('admin', '2318e1c272e03d25f8eac800b34b99e3', '1');
-- 初始化配置
insert into config(key, value) values('allow_white_list', '0');
insert into config(key, value) values('allow_ssl', "0");
insert into config(key, value) values('address', '')
insert into config(key, value) values('username', '');
insert into config(key, value) values('password', '');
insert into config(key, value) values('http', '80');
insert into config(key, value) values('https', '443');
insert into config(key, value) values('ssl_key', '');
insert into config(key, value) values('ssl_pem', '');
insert into config(key, value) values('app', '8080');
-- 初始化菜单
insert into menu(menu_id, menu_name, sort) values('dashboard', '仪表盘', '1');
insert into menu(menu_id, menu_name, sort) values('image-list', '镜像列表', '2');
insert into menu(menu_id, menu_name, sort) values('container-list', '容器列表', '3');
insert into menu(menu_id, menu_name, sort) values('user-manage', '用户管理', '4');
insert into menu(menu_id, menu_name, sort) values('system-setting', '系统设置', '5');
insert into menu(menu_id, menu_name, sort) values('log-record', '操作日志', '6');
-- 提交
commit;