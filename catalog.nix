with import <nixpkgs> {};
with pkgs.python3Packages;

stdenv.mkDerivation rec {
  name = "catalog";
  version = "0.0.1";

  src = ./.;
  nativeBuildInputs = [ jedi python3 ];
  buildInputs = [ requests pyyaml flask ];
  checkInputs = [ pytest ];

  unpackPhase = "true";
  installPhase = ''
    mkdir -p $out/bin
    cp ${./src/catalog.py} $out/bin/catalog
    cp ${./src/config.yml} $out/bin/config.yml
    chmod +x $out/bin/catalog
  '';

  meta = with lib; {
    homepage = "https://github.com/rjected/bookstore";
    description = "Catalog server for CS 677";
    license = licenses.mit;
    maintainers = with maintainers; [ rjected ];
  };
}
