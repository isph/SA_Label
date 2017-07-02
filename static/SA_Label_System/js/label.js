/**
 * Created by sph on 7/2/17.
 */
var cnt = 0;
function rotate_label_image() {
    console.log(cnt);
    cnt = (cnt+1)%4;
    document.getElementById("label_image").style.transform="rotate("+cnt*90+"deg)";
}