# author: frank
# create-time:2024/3
# usage:  hook app's A/B 判断条件，用来进入一个APP的B面
#         需要配合root过，并且安装了frida服务端的模拟器使用
#         修改记录: 2024/11/7  增加时间戳，调整排版，看起来更整齐
#
import time
from datetime import datetime

import frida,sys
import os

COLORS = {
    'OKGRAP': '\033[95m',   # 紫色
    'OKBLUE': '\033[94m',   # 蓝色
    'OKGREEN': '\033[92m',  # 绿色
    'WARNING': '\033[93m',  # 黄色
    'FAIL': '\033[91m',     # 红色
    'INFO': '\033[96m',     # 青色
    'BOLD': '\033[1m',      # 加粗
    'ENDC': '\033[0m',      # 结束颜色代码
}

jscode = """

/*** Java.perform是frida的api函数,可以将其中的脚本注入到java运行库,
     参数是一个匿名函数,函数的主体内容是监控和修改java函数逻辑的主题内容,
     任何针对java层的操作都必须在这个api函数中 ***/
     
Java.perform(function()
{
    // 【1】 Hook NetworkCapabilities类的hasTransport方法
    try
    {
        var NetworkCapabilities = Java.use('android.net.NetworkCapabilities');
        NetworkCapabilities.hasTransport.overload('int').implementation = function (transportType) 
        {
            send('r--------调用NetworkCapabilities.hasTransport 0:手机网络,1:wifi,2:bt,3:internet,4:vpn,传入的Type: ' + transportType);
            var result = this.hasTransport(transportType);
            if(transportType === 4)
            {
                return false;
            }
            else if(transportType === 1)
            {
                return false;
            }
            else 
            {
                return true;
            }
        };
    }
    catch (e) {
        send("r--------调用NetworkCapabilities类的hasTransport方法, error: " + e.message);
    }
    
    // 【2】 Hook Settings.Global类的getInt方法
    try
    {
        var SettingsGlobal = Java.use('android.provider.Settings$Global');
        SettingsGlobal.getInt.overload('android.content.ContentResolver', 'java.lang.String').implementation = function (resolver, name) {
            send('a--------调用Settings.Global.getInt()，获取属性:' + name);
            // 调用原始方法获取返回值
            // var result = this.getInt(resolver, name);
            var result = 0;
            send('a--------调用Settings.Global.getInt 强制返回: ' + result);
            return result;
        };
    }
    catch (e) {
        send("r--------hook Settings.Global类的getInt方法, error: " + e.message);
    }
    
    // 【3】 Hook Context类的registerReceiver方法 和 getSystemService方法
    try
    {
        var Context = Java.use('android.content.Context');
        Context.registerReceiver.overload('android.content.BroadcastReceiver', 'android.content.IntentFilter').implementation = function (receiver, filter) {
            send('y-------------registerReceiver called IntentFilter:'+ filter);
            // 如果 IntentFilter 的 action 是 "com.example.MY_ACTION"，则返回 null
            if (filter != null && filter.hasAction("android.hardware.usb.action.USB_STATE")) {
                send("r--------------registerReceiver 监控到USB_STATE, 返回null");
                return null;  // 满足条件时返回 null
            }
            return this.registerReceiver(receiver, filter);  // 调用原始方法
        };
        
        Context.getSystemService.overload('java.lang.String').implementation = function(name) {
            send('y-------------Context.getSystemService被调用，sevice name:', name);
            return this.getSystemService(name);
        };
    }
    catch (e) {
        send("r--------hook Context类, error: " + e.message);
    }
    
    // 【4】 Hook DexFile的构造函数
    try
    {
        var DexFile = Java.use('dalvik.system.DexFile');
        DexFile.$init.overload('java.lang.String').implementation = function(path) {
            send("r--------DexFile构造函数被调用，路径: " + path);
            return this.$init(path);
        };
        // 如果有其他重载的构造函数，可以继续添加钩取
        DexFile.$init.overload('java.io.File').implementation = function(file) {
            send("r--------DexFile构造函数被调用，传入file:" + file);
            return this.$init(file);
        };  
    }
    catch (e) {
        send("r--------hook DexFile, error: " + e.message);
    }


    // 【5】 Hook DexClassLoader类的构造函数，看是否有载入Dex
    try
    {
        var DexClassLoader = Java.use('dalvik.system.DexClassLoader');
        DexClassLoader.$init.overload('java.lang.String', 'java.lang.String', 'java.lang.String', 'java.lang.ClassLoader').implementation = function (dexPath, optimizedDirectory, librarySearchPath, parent) 
        {
            send("r========DexClassLoader初始化，dex路径: " + dexPath);
            return this.$init(dexPath, optimizedDirectory, librarySearchPath, parent);
        };
    }
    catch (e) {
        send("r--------hook Java类:DexClassLoader, error: " + e.message);
    }
    
    // 【6】hook Java类:java.net.URL
    try
    {
        var URL = Java.use('java.net.URL');
        URL.$init.overload('java.lang.String').implementation = function (urlString) 
        {
            send('r----URL 构造函数输入参数:' + urlString);
            console.log(Java.use('android.util.Log').getStackTraceString(Java.use('java.lang.Exception').$new()));
            return this.$init(urlString);
        };
    }
    catch (e) {
        send("r--------hook Java类:java.net.URL Error: " + e.message);
    }
    
    // 【7】hook Java类:java.lang.Runtime
    try
    {
        var Runtime = Java.use('java.lang.Runtime');
        var getRuntime = Runtime.getRuntime;
        // hook Java类:java.lang.Runtime 的 exec方法
        Runtime.exec.overload('[Ljava.lang.String;', '[Ljava.lang.String;').implementation = function(cmdArray, envp) {
            send('r----Runtime.exec被调用，输入参数: ' + cmdArray + ', environment: ' + envp);
            return this.exec(cmdArray, envp);
        };
    }
    catch (e) {
        send("r--------hook Java类:java.lang.Runtime Error: " + e.message);
    }
    
    // 【8】hook Java类:java.util.Locale
    var Locale = Java.use('java.util.Locale');
    // 【8.1】hook Java类:java.util.Locale 的 toString() 方法
    Locale.toString.overload().implementation = function() {
        var locale1 = "localetostring";
        send('a--------Hook Locale.toString() 返回 '+locale1);
        return locale1;
    };
    
    // 【8.2】hook Java类:java.util.Locale 的 getCountry() 方法
    Locale.getCountry.overload().implementation = function() {
        var locale2 = "localecountrybig";
        //send('a--------Hook Locale.getCountry() 返回 '+locale2);
        return locale2;
    };
    
    // 【8.3】hook Java类:java.util.Locale 的 getLanguage() 方法
    Locale.getLanguage.overload().implementation = function() {
        var locale3 = "localelanguage";
        //send('a--------Hook Locale.getLanguage() 返回 '+locale3);
        return locale3;
    };
    
    // 【9】hook Java类:java.util.TimeZone
    var TimeZone = Java.use("java.util.TimeZone");
    var timezone1 = "timezonestring";
    // hook Java类:java.util.TimeZone 的 getID() 方法
    TimeZone.getID.overload().implementation = function() {
        send('r--------Hook TimeZone.getID() 返回 '+timezone1);
        return timezone1;
    };
    
     // 【10】hook Java类:java.lang.System的getProperty方法
    var System = Java.use('java.lang.System');
    // Hook System.getProperty 方法
    System.getProperty.overload('java.lang.String').implementation = function (key) {
        send('q--------调用System.getProperty方法  key: ' + key);
        // 获取原始返回值
        var value = this.getProperty(key);
        // 根据特定的 key 来修改返回值
        if (key === 'http.proxyHost' || key === 'http.proxyPort' || key === 'http.agent' ||
            key === 'https.proxyHost' || key === 'https.proxyPort' || key === 'https.agent' ||
            key === 'proxyHost' || key === 'ftp.proxyHost') {
            send('r--------调用System.getProperty方法  key: ' + key + ',返回不带代理的值');
            // 如果是 HTTP 代理相关的属性，返回空值或模拟没有代理
            if (key === 'http.proxyHost' || key === 'https.proxyHost' ||
                key === 'proxyHost' || key === 'ftp.proxyHost') {
                return null; // 没有代理主机
            } else if (key === 'http.proxyPort' || key === 'https.proxyPort') {
                return '0';  // 代理端口为 0，表示无代理
            } else if (key === 'http.agent' || key === 'https.agent') {
                return '';  // 空的用户代理，表示没有代理
            }
        }
        // 返回原始的值（如果没有匹配的 key）
        return value;
    };
    
    
    var simoperator = "simoperatorcode";
    var countrysmall = "localecountrysmall";
    // 【11】hook Java类:SystemProperties.get方法
    var SystemProperties = Java.use('android.os.SystemProperties');
    SystemProperties.get.overload('java.lang.String').implementation = function(key) {
        // 调用原始方法获取原始返回值
        var originalValue = this.get(key);
        send('g--------调用SystemProperties.get方法  key: '+key);
        // 判断是否访问了 ro.product.cpu.abilist 属性
        if (key === 'ro.product.cpu.abi' ||
            key === 'ro.product.cpu.abilist' ||
            key === 'ro.product.cpu.abilist32' ||
            key === 'ro.product.cpu.abilist64') 
        {
            send('r--------调用SystemProperties.get方法  key: ro.product.cpu.abi/abilist/abilist32/abilist64');
            return 'arm64-v8a';
        }
        else if (key === 'gsm.sim.operator.numeric') {
            send('r--------调用SystemProperties.get方法  key: gsm.sim.operator.numeric 修改为'+simoperator);
            return simoperator;
        }
        else if (key === 'gsm.operator.numeric') {
            send('r--------调用SystemProperties.get方法  key: gsm.operator.numeric  修改为'+simoperator);
            return simoperator;
        }
        else if (key === 'gsm.operator.alpha') {
            send('r--------调用SystemProperties.get方法  key: gsm.operator.alpha  修改为 AirTel');
            // 修改返回值为 arm64-v8a
            return 'AirTel';
        }
        else if (key === 'persist.sys.timezone') {
            send('r--------调用SystemProperties.get方法  key: persist.sys.timezone, new value:'+timezone1);
            return timezone1;
        }
        else if (key === 'gsm.sim.operator.iso-country') {
            send('r--------调用SystemProperties.get方法  key: gsm.sim.operator.iso-country, new value:'+countrysmall);
            return countrysmall;
        }
        else if (key === 'sys.usb.config') {
            send('r-------调用SystemProperties.get方法  key: sys.usb.config');
            return 'none';
        }
        // 返回原始值
        return originalValue;
    };

    //【12】hook Java类:TelephonyManager的相关方法
    var TelephonyManager = Java.use('android.telephony.TelephonyManager');
    try {
        TelephonyManager.getSimOperator.overload().implementation = function() {
            var oldValue = this.getSimOperator();
            var newValue = simoperator;
            send("r--------TelephonyManager.getSimOperator old value: " + oldValue+" new value:"+newValue);
            return newValue;
        };
        TelephonyManager.getNetworkOperator.overload().implementation = function() {
            var oldValue = this.getNetworkOperator();
            var newValue = simoperator;
            send("r--------TelephonyManager.getNetworkOperator old value: " + oldValue+" new value:"+newValue);
            return newValue;
        };
        TelephonyManager.getSimOperatorName.overload().implementation = function() {
            var oldValue = this.getSimOperatorName();
            var newValue = "AirTel";
            send("r--------TelephonyManager.getSimOperatorName old value: " + oldValue+" new value:"+newValue);
            return newValue;
        };
        TelephonyManager.getNetworkOperatorName.overload().implementation = function() {
            var oldValue = this.getNetworkOperatorName();
            var newValue = "AirTel";
            send("r--------TelephonyManager.getNetworkOperatorName old value: " + oldValue+" new value:"+newValue);
            return newValue;
        };
        TelephonyManager.getSimCountryIso.overload().implementation = function() {
            var oldValue = this.getSimCountryIso();
            var newValue = "localecountrybig";
            send("r--------TelephonyManager.getSimCountryIso 原始值: " + oldValue+" 修改为:"+newValue);
            return newValue;
        };
        TelephonyManager.getNetworkCountryIso.overload().implementation = function() {
            var oldValue = this.getNetworkCountryIso();
            var newValue = "localecountrybig";
            send("r--------TelephonyManager.getNetworkCountryIso old value: " + oldValue+" new value:"+newValue);
            return newValue;
        };
    }
    catch (e) {
        send("r--------hook Java类:TelephonyManager的相关方法 Error: " + e.message);
    }

    //【13】hook Java类:android.webkit.WebView的相关方法
    try
    {
        var WebView = Java.use("android.webkit.WebView");
        WebView.loadUrl.overload('java.lang.String').implementation = function(url)
        {
            send("r========WebViewWebView.loadUrl:" + url);
            this.loadUrl(url);
        }
    }
    catch (e) {
        send("r--------Hook android.webkit.WebView Error: " + e.message);
    }
    
    // kill当前APP所在的进程，强行退出APP
    function terminateApp() {
        var kill = Module.findExportByName("libc.so", "kill");
        var getpid = Module.findExportByName("libc.so", "getpid");
        if (kill && getpid) {
            var kill_func = new NativeFunction(kill, 'int', ['int', 'int']);
            var getpid_func = new NativeFunction(getpid, 'int', []);
            var pid = getpid_func();  // 获取当前进程ID
            send("r----------------强行终止APP,进程ID:"+pid);
            kill_func(pid, 9);  // 发送 SIGKILL (9) 信号给当前进程
        }
        else
        {
            send("r----------------强行终止APP失败");
        }
    }
    
    //【14】hook libc.so的remove方法
    var remove = Module.findExportByName("libc.so", "remove");
    if (remove !== null) {
        Interceptor.attach(remove, {
            onEnter: function (args) {
                var path = Memory.readUtf8String(args[0]);
                send("r--------试图删除文件: " + path);
                if(path.includes(".jar"))
                {
                    //terminateApp();
                }
            },
            onLeave: function (retval) {
            }
        });
    } else {
        console.log("libc remove not found.");
    }
    
    //【15】hook libc.so的__system_property_get方法
    var propertyName = "";
    var arg1 ="";
    Interceptor.attach(Module.findExportByName("libc.so", "__system_property_get"), {
        onEnter: function(args) {
            // 从第一个参数中获取属性名称
            propertyName = Memory.readUtf8String(args[0]);
            arg1 = args[1];
            if(propertyName == "ro.product.brand")
            {
            }
            else if(propertyName == "gsm.operator.numeric")
            {
            }
            else if(propertyName == "ro.product.cpu.abilist" || propertyName == "ro.product.cpu.abilist32" || propertyName == "ro.product.cpu.abilist64") 
            {
            }
            if(path.includes("persist.nox") || path.includes("debug.hwui"))
            {
            }
            else
            {
                send("a---- __system_property_get被调用，属性名称:"+ propertyName);
            }
            
        },
        onLeave: function (retval) {
            if (propertyName === "gsm.operator.numeric") {
                send("r---- hook gsm.operator.numeric 将返回的字符串修改为 40551");
                Memory.writeUtf8String(arg1, "40551");
            }
            else if (propertyName === "gsm.sim.operator.numeric") {
                send("r---- hook gsm.sim.operator.numeric 将返回的字符串修改为 40551");
                Memory.writeUtf8String(arg1, "40551");
            }
            else if (propertyName === "ro.product.cpu.abilist" ||
                     propertyName === "ro.product.cpu.abilist32" ||
                     propertyName === "ro.product.cpu.abilist64") 
            {
                send("r--------hook __system_property_get, key:ro.product.cpu.abilist/abilist32/abilist64 将返回的字符串长度修改为 9");
                retval.replace(9);
                send("r--------hook __system_property_get, key:ro.product.cpu.abilist/abilist32/abilist64 将返回的字符串修改为 arm64-v8a");
                Memory.writeUtf8String(arg1, "arm64-v8a");
            }
            else if (propertyName === "gsm.sim.operator.iso-country")
            {
                send("r--------hook gsm.sim.operator.iso-country 将返回的字符串修改为 in");
                Memory.writeUtf8String(arg1, "in");
            }
            else if (propertyName === "sys.usb.config")
            {
                send("r--------hook sys.usb.config 将返回的字符串修改为 charge");
                Memory.writeUtf8String(arg1, "none");
            }
        }
    });

    //【16】hook libc.so的access方法
    Interceptor.attach(Module.findExportByName(null, 'access'),
    {
        onEnter: function (args) {
        var fileName = Memory.readCString(args[0]);
        if(path.includes("lib64"))
        {}
        else{
            send('g----发现要访问 '+fileName);
        }
        if (fileName === '/system/lib/libhoudini.so' || 
            fileName === '/sdcard/_dwyq' ||
            fileName === '/sbin/su' ||
            fileName === '/system/bin/su' ||
            fileName === '/system/sbin/su' ||
            fileName === '/vendor/bin/su' ||
            fileName === '/system/xbin/su' ||
            fileName === '/data/local/xbin/su' ||
            fileName === '/data/local/bin/su' ||
            fileName === '/system/sd/xbin/su' ||
            fileName === '/system/bin/failsafe/su' ||
            fileName === '/system/xbin/busybox' ||
            fileName === '/system/app/Superuser.apk' ||
            fileName === '/data/local/su' ) {
          this.shouldModify = true;
          if(path.includes("lib64"))
          {
          }
          else{
            send('r----发现要访问 '+fileName);
          }
          
        } else {
          this.shouldModify = false;
        }
        },
        onLeave: function (retval) {
            if (this.shouldModify) {
              console.log('============修改access返回值为-1');
              retval.replace(-1);
            }
        }
    });

})
"""
start_time = None
def print_color_log(message, color):
    global start_time
    current_time = int(time.time() * 1000)  # 获取当前时间戳（毫秒）
    if start_time is None:
        start_time = current_time  # 第一条日志的时间戳
    delta_time = current_time - start_time  # 计算当前日志与第一条日志的时间差
    delta_time_str = f"{delta_time:04d}"  # 格式化为4位数
    print(COLORS[color] + f"[{delta_time_str}ms]" + message + COLORS['ENDC'])

# js中执行send函数后要回调的函数，用来打印彩色log
def on_message(message, data):
    if message["type"] == "send":
        log = message["payload"]
        if log.startswith("g"):
            print_color_log(message["payload"][1:],"OKGREEN")
        elif log.startswith("y"):
            print_color_log(message["payload"][1:],"WARNING")
        elif log.startswith("r"):
            print_color_log(message["payload"][1:], "FAIL")
        elif log.startswith("a"):
            print_color_log(message["payload"][1:], "OKGRAP")
        elif log.startswith("q"):
            print_color_log(message["payload"][1:], "INFO")


process = frida.get_usb_device()
package_name = 'com.ilyass.sloppycrash'

country = 'india'
# country = 'brazil'

pid = process.spawn([package_name])
jscode = jscode.replace("com.passympa.princessteen", package_name)
if country == 'india':
    jscode = jscode.replace("localetostring", "hi_IN")
    jscode = jscode.replace("localecountrybig", "IN")
    jscode = jscode.replace("localecountrysmall", "in")
    jscode = jscode.replace("localelanguage", "hi")
    jscode = jscode.replace("timezonestring", "Asia/Kolkata")
    jscode = jscode.replace("simoperatorcode", "40551")
elif country == 'brazil':
    jscode = jscode.replace("localetostring", "pt_BR")
    jscode = jscode.replace("localecountrybig", "BR")
    jscode = jscode.replace("localecountrysmall", "br")
    jscode = jscode.replace("localelanguage", "pt")
    jscode = jscode.replace("timezonestring", "America/Sao_Paulo")
    jscode = jscode.replace("simoperatorcode", "72408")
    jscode = jscode.replace("AirTel", "TIM (Telecom Italia)")

session = process.attach(pid)               # 加载进程号
script = session.create_script(jscode)      # 创建js脚本
script.on('message', on_message)            # 加载回调函数，也就是js中执行send函数规定要执行的python函数
script.load()                               # 加载脚本
process.resume(pid)                         # 重启app
sys.stdin.read()

