### Hi Ms Hannah!
### If you see these lines, i hope you have a nice day!

This is **README** file to explains how to set up the **environment** and run the **scripts**.

<h1 style="color:#fe9600;"> Prequisites: </h1>

 - Use **Python** for supporting Selenium
 - Set up IDE on **Visual studio code**
 - Install and configure Selenium Webdriver
 - Choose **Chrome** for Browser, ensure the correct Webdriver
 - Manage project dependency by **Pip**
 - Use **Github** for version control system


<h1 style="color:#fe9600;"> Step to run code: </h1>

 - Create **Conftest.py** to set up **Chrome** driver
    - I have set up **ChromeDriver** by install driver from internet and added it into the environment field in my laptop
    - Please remember *import pytest* and *@pytest.mark.usefixtures("driver")* before you use each module!

 - Run each test case you want, but may be you will see **Cloudflare** force you to verify "Im a human". It will hidden your process testing when code is running. You can try to download **Opencart** in localhost to fix this error!
 - Maybe you can see some failed testcase, but it's not your fault, the reason is **OpenCart** has problem!
 - Code will create report.html if you run **pytest --html=report.html**, please take a look to see the run time, number of test cases with specific failed and passed errors
 - In my Selenium script, there might be numerous time.sleep() statements at various stages. This is because, during testing over the internet, Cloudflare frequently appears and performs human verification. This causes certain button and field attributes to remain hidden temporarily, requiring me to set time.sleep() to wait for these elements to appear.






