package forwardauth

test_allow_search_analyst {
  input := {"user":"dev","roles":["analyst"],"path":"/search?q=info","method":"GET","labels":{}}
  allow with input as input
}
