//TODO: Encrypt user input for account creation during transit.
async function create_user(username, email, password){
  const res = await fetch('http://localhost:8000/auth/', {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, email, password }),
  });
  if (!res.ok) throw new Error(await res.text());
}

//FIX: Can create account without inputing username, email and password.
document.getElementById("submit").onclick = async function(){
 const username = document.getElementById("username").value;
 const email = document.getElementById("email").value;
 const password = document.getElementById("password").value;
 const status = document.getElementById("status");

  try {
    await create_user(username, email, password);
    status.textContent = "User created.";
    window.location.replace("http://localhost:8000/home")
  } catch (err) {
    status.textContent = "Failed: " + err.message;
  }
};

document.getElementById("login").onclick = async function(){
  const username = document.getElementById("login-username").value;
  const password = document.getElementById("login-password").value;
  const status = document.getElementById("login-status").value;

  try {
    
  }
}
