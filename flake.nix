{
  description = "Development shell for backend and DDD learning labs";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { nixpkgs, ... }:
    let
      systems = [
        "x86_64-linux"
        "aarch64-linux"
        "aarch64-darwin"
        "x86_64-darwin"
      ];
      forAllSystems = nixpkgs.lib.genAttrs systems;
    in {
      devShells = forAllSystems (system:
        let
          pkgs = import nixpkgs { inherit system; };
        in {
          default = pkgs.mkShell {
            packages = [
              pkgs.python3
              pkgs.go
              pkgs.jdk
              pkgs.nodejs
            ];

            shellHook = ''
              echo "learning-backend-ddd dev shell"
              echo "Try: python3 projects/task-api-stdlib/test_domain.py"
              echo "Try: cd projects/go-http-api && go test ./..."
              echo "Try: node projects/graphql-local-api/server.test.mjs"
            '';
          };
        });
    };
}
