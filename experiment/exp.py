import json

a_dict={
    "a":1,
    "b":[1,2,3,4],
    "c":{
        "ca":1,
        "cb":[1,2,3,4],
        "cc": "",
        "cd":[{"cda":"","cdb":""},{"ff":"ff","gg":"gg"}]
    }
}


subj=json.dumps(a_dict)
print(subj)