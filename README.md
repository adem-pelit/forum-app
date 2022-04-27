# forum-app
Staj mülakatı için geliştirdiğim forum sitesi uygulamasıdır. sitenin backend kısmı için python dili ve flask frameworkü, veritabanı için mysql veritabanı, frontend kısmı için ise html css ve js kullanılmıştır.

## kurulum

localhostta çalıştırmak isterseniz cihazınızda Python yüklü olmalıdır. Projede kullanılan sürüm 3.9.10 sürümüdür.
```
cd project_folder_path
pip install -r requirements.txt
```
komutuyla gerekli kütüphaneler yüklenmelidir.
```
flask run --host=0.0.0.0
```
komutu ile de uygulamayı çalıştırabilirsiniz.

## Site içeriği

### /login ve /signin sayfaları
siteye ilk defa gelindiğinde kullanıcıyı login sayfası karşılar. Kullanıcı kayıt yaptıysa bilgilerini girerek ana sayfaya gidebilir. Yada "I dont have an account" yazısına tıklayarak yeni hesap açmak için signin sayfasına gidebilir.

![image](https://user-images.githubusercontent.com/55463533/165632391-d551fcf3-b75f-4521-9b19-9a0776e51979.png)

### ANASAYFA

Kullanıcı giriş yaptığında karşınısına anasayfa çıkacaktır. Bu sayfada açılan bütün başlıklar sıralanmaktadır. Kullanıcı istediği takdirde paylaşın kısmından yeni bir başlık açabilir. Bunun için konunun başlığını ve açıklamasını yazması yeterlidir.

![image](https://user-images.githubusercontent.com/55463533/165632866-83e58311-3aae-4918-9da7-567a846ada32.png)

Örnek bir başlık alt taraftaki gibi görünür. Kullanıcı veya admin başlığı ![image](https://user-images.githubusercontent.com/55463533/165633678-a9ff55fa-37d7-44ce-9d45-ea820d1be4d6.png) butonu ile silebilir, ![image](https://user-images.githubusercontent.com/55463533/165633847-6627876f-fbaa-46f2-915f-5dec20cad6ee.png) butonu ile de yoruma kapatabilir. kullanıcı ismine tıklanarak kullanıcı bilgilerinin olduğu sayfaya gidilebilir. Kullanıcı yorumları görmek istediğinde başlığın herhangi bir yerine tıklayarak o başlığa özel sayfaya giderek başlığa yapılan yorumları görebilir.

![image](https://user-images.githubusercontent.com/55463533/165633560-0bc67917-38a9-4f7c-b455-a79898b6687d.png)

### Başlık sayfası

Başlık sayfasında bir başlık ve başlık için yapılan yorumlar bulunmaktadır. Kullanıcı başlığa yorum yapabilir, yapılan yorumları yanıtlayabilir, kendi yorumlarını silebilir. Yanıtlama örneği aşağıdaki gibi gösterilebilir.

![image](https://user-images.githubusercontent.com/55463533/165635513-d7af63e5-fc7c-4775-9c2b-56a65f6039ae.png)

Başlık yorum yapma seçeneği kapatılınca bu şekilde görünecektir.

![192 168 1 101_5000_post_id=83](https://user-images.githubusercontent.com/55463533/165635997-8cf49e51-3b86-4b63-b9bb-cb20c7192c06.png)

### Hakkımda sayfası

Hakkımda sayfası kullanıcı bilgilerinin bulunduğu sayfadır. Bu sayfada kullanıcının açtığı başlıklar da sıralanmaktadır.

![192 168 1 101_5000_user_name=adempelit (2)](https://user-images.githubusercontent.com/55463533/165638110-bbdd7536-f2a9-4a0f-b900-d39a7fffe49e.png)
