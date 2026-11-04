async function create_post(content){
  const res = await fetch('http://localhost:8000/posts', {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({content}),
  });
  if (!res.ok) throw new Error(await res.text());
}
//FIX: Goes to a web page that doesn't exist to post messages.
document.getElementById("post").onClick = async function(){
   const content = document.getElementbyId("post-text").value;
   console.log("Post input received")
   const status = document.getElementbyId("status");

    try {
    console.log("Awaiting post request");
    await create_post(content);
    console.log("Post successful");
  } catch (err) {
    status.textContent = "Failed: " + err.message;
  }
};
