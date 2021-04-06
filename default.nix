{ pkgs ? import <nixpkgs> {} }:
pkgs.mkShell {
  nativeBuildInputs = [
    pkgs.python3Packages.flask
    pkgs.python3Packages.requests
    pkgs.python3Packages.pyyaml
    pkgs.python3Packages.jedi
  ];
}
