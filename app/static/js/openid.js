/**
 * Created with PyCharm.
 * User: avtierzov@gmail.com
 * Date: 13.12.14
 * Time: 20:05
 */

function set_openid(openid, pr) {
    u = openid.search('<username>');
    if (u != -1) {
        // openid requires username
        user = prompt('Enter your ' + pr + ' username:');
        openid = openid.substr(0, u) + user;
    }
    form = document.forms['login'];
    form.elements['openid'].value = openid;
}