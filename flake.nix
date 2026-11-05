{
    inputs.nixpkgs.url = "nixpkgs";

    outputs = { nixpkgs, ... }:
        let
            pkgs = nixpkgs.legacyPackages.x86_64-linux;
            python = pkgs.python313.withPackages (ps: with ps; [
                numpy
                matplotlib
            ]);
        in {
            packages.x86_64-linux.default = pkgs.writeShellApplication {
                name = "vial";
                runtimeInputs = [ python ];
                text = ''
                    export PYTHONPATH="${./.}:''${PYTHONPATH:-}"
                    exec ${python}/bin/python ${./main.py} "$@"
                '';
            };

            devShells.x86_64-linux.default = pkgs.mkShell {
                packages = [ python ];
            };
        };
}
