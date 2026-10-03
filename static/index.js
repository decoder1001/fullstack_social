//TODO: Encrypt user input for account creation during transit.
async function create_user(username, email, password){
  const res = await fetch('http://localhost:8000/auth/', {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, email, password }),
  });
  if (!res.ok) throw new Error(await res.text());
}
//WARNING: a token is being created before user input login credentials.
//         a token attempt to be created when clicked anywhere in HTML form field.
async function login_for_access_token(username, password){
  const res = await fetch('http://localhost:8000/auth/token', {
    method: "POST",
    body: new URLSearchParams({username, password}),
  });
  if (!res.ok) throw new Error(await res.text());
  const { access_token } = await res.json();
  return access_token;
}

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
  const loginstatus = document.getElementById("loginstatus");

  //TODO: Encrypt user credentials during transit
  //      Make seperate instantes of /home for each user with their info 

  try {
    const token = await login_for_access_token(username, password);
    loginstatus.textContent = `Logged in.`;
    window.location.replace("http://localhost:8000/home")
  } catch (err) {
    loginstatus.textContent = "Failed: " + err.message;
  }
};
