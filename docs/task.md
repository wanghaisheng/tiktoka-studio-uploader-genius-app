task planning 





use case 1:bootstrap channel

if you wanna run a test against youtube algorithm, you prepared 100 video files


1. lets say you got 1 fresh account.

when import video assets and create a task,you can use mode=='单平台单账号',it will publish all these 100 videos under the same account in future. through daily limit and schedule date hour you can set it to publish one or more videos at different time

2. lets say you got 2 fresh account.one is main account and the other is backup one, backup means if upload to the main failed,we try to upload it to backup one.

when import video assets and create a task,you can use mode=='同平台主副账号' and bind the main account only,we can auto detect the bindship  whether main account has a backup one,in the beginning it will try to upload all these 100 videos under the main account in future and you will find the failed other video in the backup account. through daily limit and schedule date hour you can set it to publish one or more videos at different time

2. lets say you got 5 fresh account.each one is indepedent.你有2种选择，
第一种选择，“单平台多独立账号平均发布”，将100个视频平均分配到5个账号，每个账号20个视频，

第二种选择，“单平台多独立账号独立发布”，将100个视频分配到5个账号，每个账号100个视频，




use case 2:mature stage

after some days tests,you find out the true spoiled channel by youtube algorithm,you can set up upload regularly now 

