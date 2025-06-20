{
  description = "Nix flake for running zotero2readwise script";
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  inputs.poetry2nix.url = "github:nix-community/poetry2nix";

  outputs = { self, nixpkgs, poetry2nix }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
      inherit (poetry2nix.lib.mkPoetry2Nix { inherit pkgs; }) mkPoetryApplication defaultPoetryOverrides;
      zotero2readwise = mkPoetryApplication {
        projectDir = ./.;
        # Pyzotero requires setuptools.
        # https://github.com/nix-community/poetry2nix/blob/master/docs/edgecases.md
        overrides = defaultPoetryOverrides.extend (final: prev: {
          pyzotero = prev.pyzotero.overridePythonAttrs ( old: {
            buildInputs = (old.buildInputs or [ ]) ++ [ prev.setuptools ];
          });
        });
      };
    in
    {
      apps.${system}.default = {
        type = "app";
        # replace <script> with the name in the [tool.poetry.scripts] section of your pyproject.toml
        program = "${zotero2readwise}/bin/run";
      };
    };
}