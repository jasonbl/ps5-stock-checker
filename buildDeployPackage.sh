sources=(stockChecker.py PlaystationSeller.py textSender.py)

python3 -m pip install -r requirements.txt -t dependencies
cd dependencies || exit
zip -r ../deployment-package.zip .
cd ..
rm -rf dependencies

for source in "${sources[@]}"
do
  zip -r -g deployment-package.zip "$source"
done
