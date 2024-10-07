{
  description = "Nix flake for running zotero2readwise script";
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs";
    flake-parts.url = "github:hercules-ci/flake-parts";
  };

  outputs = { self, nixpkgs, flake-parts }:
    flake-parts.lib.mkFlake { systems = [ "x86_64-linux" "x86_64-darwin" "aarch64-linux" "aarch64-darwin" ]; } {
      perSystem = { system, pkgs, ... }: {
        packages.default = pkgs.python3Packages.buildPythonPackage {
          pname = "zotero2readwise-runner";
          version = "0.1.0";

          src = ./.;

          buildInputs = [
            pkgs.python3Packages.pip
          ];

          propagatedBuildInputs = [];

          doInstallCheck = false;
          meta.license = pkgs.lib.licenses.mit;
        };

        apps.default = {
          type = "app";
          program = "${self.packages.${flake-parts.lib.systemToPackagesKey system}.default}/bin/python3 ${self.packages.${flake-parts.lib.systemToPackagesKey system}.default}/run.py";
        };
      };
    };
}
