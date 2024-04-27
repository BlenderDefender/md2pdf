# Invoice

<!-- Invoice example based on https://github.com/CourtBouillon/weasyprint-samples/tree/master/invoice -->

<div class="flex">

!include contact-information.md

```{.python .cb-run}
!include invoice.py
```

<div class="information">

```{.python .cb-run}
print(invoice_information)
```

</div>
</div>


<div>

```{.python .cb-run}
print(product_table)
```

</div>

<div class="footer">

```{.python .cb-run}
print("\n" + due_information + "\n")
```

</div>
