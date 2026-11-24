
from flask import Flask, render_template, request
import math

app = Flask(__name__)

def algorithms(reqs, head, size, direction):
    def movement(seq):
        total=sum(abs(seq[i]-seq[i-1]) for i in range(1,len(seq)))
        return total, seq
    results={}
    results["FCFS"]=movement([head]+reqs)

    left=sorted([x for x in reqs if x<head])
    right=sorted([x for x in reqs if x>=head])
    cur=head; seq=[head]; pending=reqs[:]
    while pending:
        nxt=min(pending,key=lambda x:abs(x-cur))
        pending.remove(nxt); cur=nxt; seq.append(cur)
    results["SSTF"]=movement(seq)

    def scan():
        l=left[:]; r=right[:]; seq=[head]
        if direction=="right":
            seq+=r
            if seq[-1] != size-1: seq.append(size-1)
            seq+=l[::-1]
        else:
            seq+=l[::-1]
            if seq[-1] != 0: seq.append(0)
            seq+=r
        return movement(seq)
    results["SCAN"]=scan()

    def cscan():
        l=left[:]; r=right[:]; seq=[head]
        if direction=="right":
            seq+=r
            if seq[-1]!=size-1: seq.append(size-1)
            seq.append(0)
            seq+=l
        else:
            seq+=l[::-1]
            if seq[-1]!=0: seq.append(0)
            seq.append(size-1)
            seq+=r[::-1]
        return movement(seq)
    results["C-SCAN"]=cscan()

    def look():
        seq=[head]
        if direction=="right": seq+=right+left[::-1]
        else: seq+=left[::-1]+right
        return movement(seq)
    results["LOOK"]=look()

    def clook():
        seq=[head]
        if direction=="right": seq+=right+(left if left else [])
        else: seq+=left[::-1]+right[::-1]
        return movement(seq)
    results["C-LOOK"]=movement(seq_clook(head,left,right,direction))
    return results

def seq_clook(head,left,right,direction):
    if direction=="right":
        return [head]+right+([left[0]]+left[1:] if left else [])
    return [head]+left[::-1]+(right[::-1] if right else [])

@app.route("/", methods=["GET","POST"])
def index():
    data=None
    if request.method=="POST":
        try:
            reqs=[int(x.strip()) for x in request.form["requests"].split(",") if x.strip()]
            head=int(request.form["head"]); size=int(request.form["size"])
            direction=request.form.get("direction","right")
            if size<2 or head<0 or head>=size or any(x<0 or x>=size for x in reqs):
                raise ValueError("All cylinders must be between 0 and disk size - 1.")
            res=algorithms(reqs,head,size,direction)
            data={k:{"movement":v[0],"sequence":v[1]} for k,v in res.items()}
            best=min(data,key=lambda k:data[k]["movement"])
            avg={k:round(v["movement"]/max(len(reqs),1),2) for k,v in data.items()}
            data["best"]=best; data["average"]=avg; data["requests"]=reqs; data["head"]=head
        except Exception as e:
            data={"error":str(e)}
    return render_template("index.html", data=data)

if __name__=="__main__":
    app.run(debug=True)
