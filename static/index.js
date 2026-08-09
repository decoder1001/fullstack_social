/*let fullName = "Ross Hyland";
//let age = 24;
let isStudent = false;

let username;

document.getElementById("mySubmit").onclick = function(){
  username = document.getElementById("myText").value;
  document.getElementById("myH1").textContent = `Hello ${username}`
*/

document.getElementById("submit").onclick = function(){
  username = document.getElementById("username").value;
  email = document.getElementById("email").value;
  password = document.getElementById("password").value;

  console.log(username);
  console.log(email);
  console.log(password);
}
