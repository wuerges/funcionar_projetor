
# gerar stream
cvlc screen:// :screen-fps=10 --sout '#transcode{vcodec=DIV3,vb=4000,scale=1,acodec=mp3,ab=32,channels=2}:std{access=mmsh,mux=asfh,dst=:2000}'

# tocar stream

cvlc mmsh://localhost:2000
