


class StructureError(Exception):
    def __init__(self, message, **context):
        self.message = message
        self.context = context
        super().__init__(message)

    def __str__(self):
        lines = [f"Error: {self.__class__.__name__}", " |"]

        for key, value in self.context.items():
            lines.append(f" | {key}: {value}")

        lines.append(" |")
        lines.append(f" | {self.message}")

        return "\n".join(lines)
    



class TypeMismatchError(Exception):
    def __init__(self, message, **context):
        self.message = message
        self.context = context
        super().__init__(message)

    def __str__(self):
        lines = [f"Error: {self.__class__.__name__}", " |"]

        for key, value in self.context.items():
            lines.append(f" | {key}: {value}")

        lines.append(" |")
        lines.append(f" | {self.message}")

        return "\n".join(lines)


class SchemaError(Exception):
    def __init__(self, message, **context):
        self.message = message
        self.context = context
        super().__init__(message)

    def __str__(self):
        lines = [f"Error: {self.__class__.__name__}", " |"]

        for key, value in self.context.items():
            lines.append(f" | {key}: {value}")

        lines.append(" |")
        lines.append(f" | {self.message}")

        return "\n".join(lines)



class ParseError(Exception):
    def __init__(self, message, original=None, **context):
        self.message = message
        self.original = original
        self.context = context
        super().__init__(message)

    def __str__(self):
        lines = [f"Error: {self.__class__.__name__}", " |"]

        # context block
        if self.context:
            max_key = max(len(k) for k in self.context)
            for key, value in self.context.items():
                lines.append(f" | {key.ljust(max_key)} : {value}")

        lines.append(" |")

        # main message
        lines.append(f" | {self.message}")

        # original er$ror
        if self.original:
            lines.append(" |")
            lines.append(f" | {self.original}")

        return "\n".join(lines)
    












class BaseError(Exception):
    def __init__(self, message: str, *, error_type: str, **context):
        self.message = message
        self.error_type = error_type
        self.context = context
        super().__init__(message)

    def __str__(self):
        lines = [f"Error: {self.error_type}", " |"]

        for k, v in self.context.items():
            lines.append(f" | {k}: {v}")

        lines.append(" |")
        lines.append(f" | {self.message}")

        return "\n".join(lines)




class ErrorContext:
    def __init__(self, **base):
        self.base = base

    def error(self, message: str, error_type: str, **extra):
        return BaseError(
            message,
            error_type=error_type,
            **{**self.base, **extra}
        )




class ErrorReport(Exception):
    def __init__(self):
        self.errors: list[BaseError] = []

    def add(self, error: BaseError):
        self.errors.append(error)

    def __str__(self):
        return "\n\n".join(str(e) for e in self.errors)





if __name__ == "__main__":

    # Error → atomic (one failure)
    e = BaseError(
        "The namespace file could not be located",
        error_type="EntityNotFound",
        file="entities/foo.json",
        package="test",
    )
    
    # Print the string representation of the error
    #print(e)


    ctx = ErrorContext(
        package="nginx",
        release="1.2.0"
    )

    report = ErrorReport()

    report.add(ctx.error(
        "Entity file not found",
        error_type="EntityNotFound",
        path="entities/foo.json"
    ))

    report.add(ctx.error(
        "Invalid compiler",
        error_type="ValidationError",
  
    ))

    if report.errors:
        print(report)