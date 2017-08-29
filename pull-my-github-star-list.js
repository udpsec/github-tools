var fs = require('fs');
var child_exe = require('child_process');

child_exe.exec('curl -o starred.json -u username:password https://api.github.com/users/yangfch3/starred?per_page=500&page=1', function(err, stdout, stderr) {
    console.log(stdout);
    // 同步读取文件
    var src = fs.readFileSync('./starred.json', 'utf-8');

    var jsonArray = JSON.parse(src);
    console.log(typeof jsonArray);

    var box = '';

    for (var i = 0; i < jsonArray.length; i++) {
        var txtEle = '[' + jsonArray[i].full_name + ']' + '(' + jsonArray[i].html_url + ')' + '\n' + ':    ' + jsonArray[i].description + '\n\n';
        box += txtEle;
    }

    var file = "./output.md";
    fs.appendFile(file, box, function(err) {
        if (err)
            console.log("fail " + err);
        else
            console.log("写入文件ok");
    });

    child_exe.exec('del starred.json', function(err, stdout, stderr) {
        console.log(stdout);
    });
});