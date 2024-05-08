# -----------------------------------------------------------------------------
# Generate help output when running just `make`
# -----------------------------------------------------------------------------
.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

help:
	@python3 -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

# -----------------------------------------------------------------------------


up:  ## Docker up
	docker-compose up

down:  # Docker down
	docker-compose down

optimize_pngs:  ## Optimize PNGs
	find . -name 'docs/img/*.png' -exec pngquant 64 --ext .png -f --skip-if-larger {} \;

optimize_jpgs:  ## Optimize JPGs
	open -a ImageOptim docs/img

build:  ## Build docs
	docker exec -it python-vimeo-utils_mkdocs mkdocs build
