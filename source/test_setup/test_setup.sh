#!/bin/bash

# David Lettier (C) 2013.
# Setups up the test files for CryptoHopper and CryptoShouter.

echo "Executing test script."

t=" Lorem ipsum dolor sit amet, nisl eu velit est sit morbi et, vehicula feugiat malesuada facilisi sit odio magna, quibusdam mus mi dui mauris, magna auctor sed pellentesque libero magna dignissim. In dui etiam, adipiscing bibendum. Duis imperdiet, morbi integer blandit massa nunc tincidunt et, fusce sed mattis sit vel at convallis, egestas litora arcu ullamcorper. Integer malesuada nec ut purus duis justo, pede sapien sit pede velit morbi, iaculis morbi, risus integer viverra praesent, ante eu augue mattis sed velit. Pellentesque vestibulum ligula, egestas nulla vestibulum et ipsum elit, ligula risus nulla ultricies ut orci posuere. Purus erat maecenas at maecenas pharetra, arcu vehicula in justo taciti mi, a morbi curae, integer sit habitasse at. Sagittis ridiculus id nostra netus semper, primis wisi, fusce non litora non urna id placerat, placeat orci leo orci accumsan pellentesque amet, laoreet eget pellentesque ornare pharetra morbi vestibulum. Enim scelerisque nullam erat natoque viverra pede. Aliquam nibh dolor, molestie auctor. Sagittis laoreet sed per et sollicitudin, sodales at erat morbi massa elit, ultricies nulla quam blandit lacus eget, nunc sed nulla amet aliquam lorem. Ante a. Nam habitasse egestas vel vestibulum cum quis, ac sed, erat mauris auctor orci laborum eget massa. Natoque curabitur non amet adipiscing sit. Ac condimentum nunc. Urna conubia suspendisse massa cras etiam, quam felis ipsum ut vel maecenas, potenti arcu mauris ipsum quam, vel turpis enim vitae at. Quis hendrerit nec id. Quis sapien aut vehicula facilisis sed, in congue, turpis sapien euismod, malesuada sed, ullamcorper integer et nec scelerisque. Elementum pede sodales sit, rhoncus sit ipsum. Scelerisque aliquet ac. Donec morbi cum, nec dui placerat nibh amet ut, sapien venenatis nec et at, dolorem nec diam vel purus molestie turpis.

Sapien ac orci lorem ipsum cras fusce. Nec praesent vehicula id lorem posuere vestibulum, nonummy sit curabitur. Ut erat, porttitor morbi gravida eleifend, pellentesque scelerisque arcu id fusce orci tincidunt, tempus ipsum mauris sem eu. Modi mauris a quis odio, nec vitae, quis vehicula ut vitae sed turpis. Non ultricies aliquam magna a, urna justo urna ut, pharetra tortor phasellus, natoque amet lectus est sollicitudin mauris, diam amet.

Auctor tincidunt viverra condimentum, gravida condimentum, vitae ultrices congue feugiat curae. Odio pellentesque, ultricies consequat nibh vitae dignissim quam, venenatis quisque ut volutpat vitae neque in. Orci elementum, elit luctus phasellus, massa urna ac taciti magna, turpis erat nulla ante. Donec amet. Accumsan amet lobortis velit, vulputate lorem dui sapien. Quisque cras nibh euismod vestibulum sed wisi."

if [ "$(ls -A ../out)" ]; then
	rm ../out/*.*
fi
if [ "$(ls -A ../trash)" ]; then
	rm ../trash/*.*
fi
if [ "$(ls -A ../encrypted)" ]; then
	rm ../encrypted/*.*
fi

n=0

printf "%s%s" "$t$t" > "../out/test$n.comp"
n=$(($n+1))
printf "%s%s" "$t$t" > "../out/test$n.txt"
n=$(($n+1))
printf "%s" "$t" > "../out/test$n.comp"
n=$(($n+1))
printf "%s" "$t" > "../out/test$n.txt"
n=$(($n+1))
printf "%s%s" "$t$t" > "../out/test$n.comp"
n=$(($n+1))
printf "%s%s" "$t$t" > "../out/test$n.txt"
n=$(($n+1))
printf "%s" "$t" > "../out/test$n.comp"
n=$(($n+1))
printf "%s" "$t" > "../out/test$n.txt"
n=$(($n+1))
printf "%s%s" "$t$t" > "../out/test$n.comp"
n=$(($n+1))
printf "%s%s" "$t$t" > "../out/test$n.txt"

x=6

touch -m -t 201201010000 "../out/test$x.comp"
x=$(($x+1))
touch -m -t 201201010000 "../out/test$x.txt"
x=$(($x+1))
touch -m -t 201201010000 "../out/test$x.comp"
x=$(($x+1))
touch -m -t 201201010000 "../out/test$x.txt"

touch -d "-30 days" "../trash/test_trash.comp"

echo "Done."

