# WellCTF_CTFWeb
CTF在线评测流程

欢迎提交issues
详情联系chenwm_@outlook.com

请自行在setting.py添加secret_key

环境：Django2.1+python3.5+Bootstrap3+pycharm

功能:
  用户系统：
          登陆注册系统
          用户修改密码和个人信息系统
          /admin/后台更改信息。
          后台存储用户密码的Hash值
  题目系统：
          支持所有题型，在题目弹出的模态框下载文件再提交flag即可完成提交。
  比赛系统：
          比赛系统支持根据比赛时间确定是否进行比赛
          比赛的提交情况
          first——blood系统
  战绩系统：
          可以查看用户自己成功完成的题目
          查看比赛结果
  Rank系统：
          用户可以查看top10用户
          比赛rank
  Team系统：
          支持队伍的添加、更改、创建。
          支持查看队伍排名
          
   主页：
   logo来自网上，仅作展示实例，如果有版权纠纷请联系chenwm_@outlook.com，将立即下架。
   ![image](https://github.com/lightningwm/WellCTF_CTFWeb/blob/master/image_readme/index.png)
   题目：
   添加了题型过滤器和换页按钮。
   点击题目会弹出flag提交框，提交后会有反馈显示在模态框里。
   ![image](https://github.com/lightningwm/WellCTF_CTFWeb/blob/master/image_readme/problem.png)
   ![image](https://github.com/lightningwm/WellCTF_CTFWeb/blob/master/image_readme/problem_detail.png)
   比赛：
   显示每一场比赛的可加入状态，分为个人场和团体场，没有队伍无法加入团体场。
   ![image](https://github.com/lightningwm/WellCTF_CTFWeb/blob/master/image_readme/contest.png)
   进入比赛页面可以看到详情页
   ![image](https://github.com/lightningwm/WellCTF_CTFWeb/blob/master/image_readme/contest_detail.png)
   还有比赛榜单，显示每题的一血情况和总排名情况。
   ![image](https://github.com/lightningwm/WellCTF_CTFWeb/blob/master/image_readme/contest_board.png)
   队伍：
   可以进行队伍的创建、加入和退出。
   ![image](https://github.com/lightningwm/WellCTF_CTFWeb/blob/master/image_readme/team.png)
   ![image](https://github.com/lightningwm/WellCTF_CTFWeb/blob/master/image_readme/team_in.png)
   个人信息页：
   查看个人账户信息和队伍信息
   现在还可以查看以往的做题情况和比赛记录。
   可以进行密码的修改。
   ![image](https://github.com/lightningwm/WellCTF_CTFWeb/blob/master/image_readme/profile.png)
   
