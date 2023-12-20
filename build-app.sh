SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)

echo "Building app DUT-test"
pyinstaller --name=DUT-test --onefile --windowed "$SCRIPT_DIR"/main_GUI.py

src_img_path="$SCRIPT_DIR"/images/GUI
dst_img_path="$SCRIPT_DIR"/dist/images

echo "Downloading images from '$src_img_path' -> '$dst_img_path'"

rsync -arvP "$src_img_path" "$dst_img_path"