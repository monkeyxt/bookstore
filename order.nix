with import <nixpkgs> {};
with pkgs.python3Packages;

stdenv.mkDerivation rec {
  name = "order";
  version = "0.0.1";

  src = ./.;
  nativeBuildInputs = [ jedi python3 ];
  buildInputs = [ requests pyyaml flask ];
  checkInputs = [ pytest ];

  unpackPhase = "true";
  installPhase = ''
    mkdir -p $out/bin
    cp ${./src/order.py} $out/bin/order
    cp ${./src/config.yml} $out/bin/config.yml
    chmod +x $out/bin/order
  '';

  meta = with lib; {
    homepage = "https://github.com/rjected/bookstore";
    description = "Order server for CS 677";
    license = licenses.mit;
    maintainers = with maintainers; [ rjected ];
  };
}
